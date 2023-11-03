from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
#from rest_framework.response import Response
#from .spark import SparkSes
from .functions import *
import numpy as np
#import json

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

    def get(self, request):
#        try: 
        filter_method = request.GET.get('filter_method')
        value = request.GET.get('value')
        mini = request.GET.get('minimum', 0)
        maxi = request.GET.get('maximum', 0)
        position = int(request.GET.get('position', "1"))
        size = int(request.GET.get('size', "1"))
        number_of_fields = int(request.GET.get('set_size', "10"))
        
        next_data_link = f"http://uxlivinglab200112.pythonanywhere.com/pandas/?set_size=field1&filter_method={filter_method}&size={size}&position={position+size}&value={value}&minimum={mini}&maxi={maxi}"

        se = SearchEngine(size, position)
        rf = se.filter_by_method(filter_method, value, mini, maxi)

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
