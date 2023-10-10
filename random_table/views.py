from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
#from .spark import SparkSes
from .functions import *
import json

#spark = SparkSes("CLIENT/static/data_filter.json")

def client_home(request):
    return render(request, 'client_home.html')

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

class ClientSearch(APIView):

    def post(self, request):
        data = request.data

        df = SearchManager.getInstance().fetch_by_regex(data['column'], data['regex'] , int(data['size']))
        print("result------", len(df.index))
        # use to dict
        result = df.to_dict("records")
        return JsonResponse({'data': result}, status=200)

