from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

from .functions import *


def client_home(request):
    return render(request, 'client_home.html')

class ClientSearch(APIView):

    def get(self, request):
        try:
            column = request.GET.get('column')
            regex = request.GET.get('regex')
            size = request.GET.get('size')
            position = request.GET.get('position', "1")

            size = int(size)
            try:
                position = int(position)
            except Exception as e:
                position=1

            next_data_link = f"http://uxlivinglab200112.pythonanywhere.com/pandas/?column=field1&regex={regex}&size={size}&position={position+size}"

            df = SearchManager.getInstance().fetch_by_regex(column, regex, size, position)
            result = df.to_dict("records")
            return JsonResponse({'data': result, 'next_data_link':next_data_link}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)