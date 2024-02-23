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

class ClientSearch(APIView):
    """
    API View that responds to the client search requests
    """

    def get(self, request):
        serializer = randomTableSerializers(data=request.GET)

        if not serializer.is_valid():
            return JsonResponse({'error': serializer.errors}, status=400)
        
        api_key = serializer.validated_data.get("api_key")
        filter_method = serializer.validated_data.get('filter_method')
        value = serializer.validated_data.get('value')
        mini = serializer.validated_data.get('mini')
        maxi = serializer.validated_data.get('maxi')
        position = serializer.validated_data.get('position')
        size = serializer.validated_data.get('size')
        number_of_fields = serializer.validated_data.get('set_size')

        # Pagination link used for the 
        next_data_link = f"http://uxlivinglab200112.pythonanywhere.com/api/?set_size={number_of_fields}&filter_method={filter_method}&size={size}&position={position+math.ceil(size/10000)}&value={value}&minimum={mini}&maxi={maxi}"

        try:
            se = SearchEngine(size, position , 
                              api_key = api_key)
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
#        except Exception as e:
#            return JsonResponse({'error': str(e)}, status=500)
