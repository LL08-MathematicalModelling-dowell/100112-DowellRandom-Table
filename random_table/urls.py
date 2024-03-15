from django.urls import path
from . import views

urlpatterns = [
    #path('spark/', views.ClientAdd.as_view(), name='client_add'),
    #path('api/service/' ,  views.ClientSearchwithDowellService().as_view() , name="client_search_service"),
    path('api/', views.ClientSearch.as_view(), name='client_search'),
    path('api/without_pagination/' , views.ClientSearchWithouPagination().as_view() , name = "without_pagination"),
    path('api/service' , views.ClientSearchWithoutPaginationService().as_view() , name = "service_without_pagination")
]
