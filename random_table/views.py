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
        try:
            size = data.get("size")
            position = data.get("position")
            api_key = data.get("api_key")
            se = SearchEngine(size, position , 
                              api_key = api_key , **kwargs)
            value = data.get("value")
            mini = data.get("mini")
            maxi = data.get("maxi")
            number_of_fields = data.get("set_size")
            filter_method = data.get("filter_method")
            
            next_data_link = f"http://uxlivinglab200112.pythonanywhere.com/api/?set_size={number_of_fields}&filter_method={filter_method}&size={size}&position={position+math.ceil(size/10000)}&value={value}&minimum={mini}&maxi={maxi}"
            
            rf = se.filter_by_method(filter_method, value, mini, maxi)
        except RandomTableError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        result = []
        arr = []
        for d in rf:
                arr.append(d)
                if len(arr)==number_of_fields:
                        result.append(arr)
                        arr = []

        # reshaped = rf.values.resize((int(rf.shape[0]/number_of_fields), number_of_fields), refcheck=False)

        return JsonResponse({'data': result, 'next_data_link':next_data_link}, status=200)
        
        

class ClientSearch(APIView):
    """
    API View that responds to the client search requests
    """
    
    def get(self, request):
        serializer = randomTableSerializers(data=request.GET)

        if not serializer.is_valid():
            return JsonResponse({'error': serializer.errors}, status=400)
        
        
        response = get_random_table_result(serializer.validated_data)
        
        return response
            
            
            
class ClientSearchwithDowellService(APIView):
    
    def get(self , request):
        serializer = randomTableSerializers(data=request.GET , **{"payment" : True})
                

        if not serializer.is_valid():
            return JsonResponse({'error': serializer.errors}, status=400)
        
        auth_response = processApikey(serializer.validated_data.get("api_key"))
        if auth_response["success"]:
            if (auth_response["total_credits"] < 0):
                return JsonResponse({"error" : "You don't have enough credit"})
        else:
            return JsonResponse({"error" : auth_response })
        
        response = get_random_table_result(serializer.validated_data , **{"payment" : True})
        
        return response
        
        
#        except Exception as e:
#            return JsonResponse({'error': str(e)}, status=500)
