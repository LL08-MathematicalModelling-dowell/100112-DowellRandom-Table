from django.urls import path
from . import views

urlpatterns = [
    #path('spark/', views.ClientAdd.as_view(), name='client_add'),
    path('api/', views.ClientSearch.as_view(), name='client_search'),
]
