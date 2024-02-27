import json

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class RandomTableAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("client_search") if not settings.TEST_USE_LIVE_URL else settings.LIVE_URL
        return super().setUp()
    
    def test_nps_scale(self):
        
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "no_filtering"
        }

        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_no_api_key_provided(self):
        data = {
            "filter_method" : "no_filtering"
        }

        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(json.loads(response.content) , {"api_key" : ["This field is required."]}) 


    def test_size_lower_set_size(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "no_filtering",
            "size" : 5,
            "set_size" : 10
        }

        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("data") , []) 
        
class BetweenFilteringMethodTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.url = reverse("client_search") if not settings.TEST_USE_LIVE_URL else settings.LIVE_URL
        return super().setUp()
        
    def test_between_filtering_method(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "between",
            "size" : 2,
            "set_size" : 10,
            "mini" : 0,
            "maxi" : 90000000
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_200_OK) 
    
    def test_not_mini_maxi_set(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "between",
            "size" : 2,
            "set_size" : 10,
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)
        
    def test_not_maxi_set(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "between",
            "size" : 2,
            "set_size" : 10,
            "maxi" : 9000000
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)
        
class NotBetweenFilteringMethodTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.url = reverse("client_search") if not settings.TEST_USE_LIVE_URL else settings.LIVE_URL
        return super().setUp()
        
    def test_between_filtering_method(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "not_between",
            "size" : 2,
            "set_size" : 10,
            "mini" : 50000000,
            "maxi" : 90000000
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_200_OK) 
    
    def test_not_mini_maxi_set(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "between",
            "size" : 2,
            "set_size" : 10,
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)
        
    def test_not_maxi_set(self):
        data = {
            "api_key" : settings.DATACUBE_API_KEY,
            "filter_method" : "between",
            "size" : 2,
            "set_size" : 10,
            "maxi" : 9000000
        }
        
        response = self.client.get(self.url , data)

        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)
         
        



