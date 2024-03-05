from django.urls import path
from . import views

urlpatterns = [
    #path('spark/', views.ClientAdd.as_view(), name='client_add'),
    path('api/service/' ,  views.ClientSearchwithDowellService().as_view() , name="client_search_service"),
    path('api/', views.ClientSearch.as_view(), name='client_search'),
]
