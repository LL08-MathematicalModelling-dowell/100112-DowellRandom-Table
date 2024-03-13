from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
#from rest_framework.response import Response
#from .spark import SparkSes
from .functions import *
import numpy as np
#import json
import math

from .serializers  import randomTableSerializers
from .exceptions import RandomTableError
from .authentication import processApikey
from .utils import calculate_columns

'''
spark = SparkSes("CLIENT/static/data_filter.json")
class ClientAdd(APIView):

    def post(self, request):
        data = request.data
        print(data)
        try:
            df = spark.search_by_regex(data['column'], data['regex'] , int(data['size']))
            result = df.toJSON().collect()
            data_list = [json.loads(item) for item in result]
            return Response({'data': data_list}, status=200)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)
'''

def get_random_table_result(data , **kwargs):
        url = kwargs.get("url")
        calc_col = kwargs.get("calculate_column")
        try:
            size = data.get("size")
            position = data.get("position")
            api_key = data.get("api_key")
            value = data.get("value")
            mini = data.get("mini")
            maxi = data.get("maxi")
            number_of_fields = data.get("set_size")
            filter_method = data.get("filter_method")
            
            extra_kwargs = {
                **kwargs,
                "value" : value,
                "minimum" : mini,
                "maximum" : maxi
            }
            
            
            se = SearchEngine(size, position, number_of_fields ,  filter_method,
                              api_key = api_key , pagination= False if not url else True ,  **extra_kwargs)
            
            if url:
                next_data_link = f"{url}?api_key={api_key}&set_size={number_of_fields}&filter_method={filter_method}&size={size}&position={position+math.ceil(size/10000)}&value={value}&mini={mini}&maxi={maxi}"
            
            rf = se.total_filtered_data
        except RandomTableError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        result = []
        arr = []
        
        if calc_col:
            number_of_fields = calculate_columns(size)
            
        
        for d in rf:
                arr.append(d)
                if len(arr)==number_of_fields:
                        result.append(arr)
                        arr = []
                        
        if not result:
            return JsonResponse({"error" : f"The set_size value might to too high. See it to {len(rf)} or lower"} , status = 400)

        response = {"data" : result}
        if url:
            response["next_data_link"] = next_data_link
            
        return JsonResponse(response, status=200)
    
    
class ClientSearchBaseAPIView(APIView):
    
    custom_kwargs = {}
    pagination = True
    end_point = ""

    
    def _get_random_table(self , data , **kwargs):
        return get_random_table_result(data , **kwargs)
    
    def get_pagination_link(self):
        return "https://uxlivinglab200112.pythonanywhere.com/" + self.end_point 
    
    
    def _custom_logic(self , **kwargs):
        pass
    
    
    
    def get(self ,request):
        self.serializer = randomTableSerializers(data=request.GET)
       

        if not self.serializer.is_valid():
            return JsonResponse({'error': self.serializer.errors}, status=400)
        
        try:
            self._custom_logic()
        except RandomTableError as e:
            return JsonResponse({"error" : str(e)} , status = 400)
        
        if self.pagination:
            
            self.custom_kwargs["url"] = self.get_pagination_link()
            
        
        response = get_random_table_result(self.serializer.validated_data ,  **self.custom_kwargs)
        
        return response
        
        
        

class ClientSearch(ClientSearchBaseAPIView):
    end_point = "api"
    custom_kwargs = {"payment" : False}
   
            
            
"""            
class ClientSearchwithDowellService(ClientSearchBaseAPIView):
    
    end_point = "api/service/"
    
    def _custom_logic(self, **kwargs):
        auth_response = processApikey(self.serializer.validated_data.get("api_key"))
        if auth_response["success"]:
            if (auth_response["total_credits"] < 0):
                raise RandomTableError("You don't have enough credit")
        else:
            raise RandomTableError(f"{auth_response}")
            
    
"""       

class ClientSearchWithouPagination(ClientSearchBaseAPIView):
    pagination=False
    custom_kwargs = {"payment" : False , "calculate_column" : True}
    