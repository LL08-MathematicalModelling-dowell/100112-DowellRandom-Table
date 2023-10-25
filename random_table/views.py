from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
#from rest_framework.response import Response
#from .spark import SparkSes
from .functions import *
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
        try: 
            fields = request.GET.get('fields').split(',')
            filter_methods = request.GET.get('filter_methods').split(',')
            values = request.GET.get('values').split(',')
            position = request.GET.get('position')
            
            if len(fields) != len(filter_methods) or len(filter_methods) != len(values):
                return JsonResponse({'error': 'Mismatched number of fields, filter methods, and values'}, status=400)

            result = []

            for i in range(len(fields)):
                field = fields[i]
                filter_method = filter_methods[i]
                value = values[i]
                df = SearchManager.getInstance().fetch_by_filter(field, filter_method, value, int(position))
                result.extend(df.to_dict("records"))

            return JsonResponse({'data': result}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
