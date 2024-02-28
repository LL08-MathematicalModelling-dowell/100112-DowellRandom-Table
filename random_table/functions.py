import pandas as pd
import math  
import requests
import json


from .utils import extract_digits , check_value_integer_string
from .exceptions import DatabaseFetchError , RandomTableTypeError , RandomTableError



column = "column"
class SearchEngine:
    """
    A class that
    """
    def __init__(self, size, position , api_key= None , **kwargs):
        self.df = None
        required_collection = math.ceil(size/10000)
        if not position:
            position = 1

        dfs = []
        for i in range(position, position+required_collection):
            data = fetch('collection_'+str(i) , api_key , limit = size , **kwargs)
            if not data:
                continue
            dfs = dfs + data
        self.df = pd.Series(dfs[:size])
        
        
    def filter_by_regex(self, regex):
        
        
        df = self.df[self.df.astype(str).str.contains(regex, regex= True, na=False)]
        return df
    
    def filter_by_contains(self, value):
        if not check_value_integer_string(value):
            raise RandomTableTypeError("Value sent should of an integer type")
        value = str(value)
        
        df =  self.df[self.df.astype(str).str.contains(value, regex= False, na=False)]
        
        return df
    
    def filter_by_not_contains(self, value):
        if not check_value_integer_string(value):
            raise RandomTableTypeError("Value sent should be an integer type")
        value = str(value)
        
        df = self.df[~(self.df.astype(str).str.contains(str(value), regex= False, na=False))]
        return df
    
    def filter_by_exact(self, value):
       df = self.df[self.df == value]
       return df
    
    def filter_by_starts_with(self, value):
        if not check_value_integer_string(value):
            raise RandomTableTypeError("Value sent should be an integer type")
        value = str(value)
        df = self.df[self.df.astype(str).str.startswith(value, na=False)]
        return df
    
    def filter_by_ends_with(self, value):
        if not check_value_integer_string(value):
            raise RandomTableTypeError("Value sent should be an integer type")
        value = str(value)
        df = self.df[self.df.astype(str).str.endswith(value, na=False)]
        return df
    
    def filter_by_greater_than(self, value):
        df = self.df[self.df > int(value)]

        return df
    
    def filter_by_less_than(self, value):
        df = self.df[self.df < int(value)]

        return df
    
    def filter_by_between(self, minimum, maximum):
        df = self.df[(self.df > minimum) & (self.df< maximum)]
        return df
    
    def filter_by_not_between(self, minimum, maximum):


        min_df = self.df[self.df < minimum]
      
        max_df = self.df[self.df > maximum]
        return pd.concat([min_df,max_df])


    def filter_by_odd(self):
        df = self.df[(self.df%2!=0)]
        return df

    def filter_by_even(self):
        df = self.df[self.df%2==0]
        return df
    def filter_by_multiple_of(self, value):
        print(type(value))
        df = self.df[self.df % int(value) ==0]
        return df

    def filter_by_no_filtering(self):
        return self.df

    def filter_by_first_and_last_digits(self):
        self.df = self.df.apply(extract_digits)
        return self.df

    def filter_by_method(self, filter_method , value, minimum=None, maximum=None):
        if filter_method == 'regex':
            return self.filter_by_regex(value)
        elif filter_method == 'contains':
            return self.filter_by_contains(value)
        elif filter_method == 'not_contains':
            return self.filter_by_not_contains(value)
        elif filter_method == 'starts_with':
            return self.filter_by_starts_with(value)
        elif filter_method == 'ends_with':
            return self.filter_by_ends_with(value)
        elif filter_method == 'greater_than':
            return self.filter_by_greater_than(value)
        elif filter_method == 'less_than':
            return self.filter_by_less_than(value)
        elif filter_method == 'between':
            return self.filter_by_between(int(minimum), int(maximum))
        elif filter_method == 'not_between':
            return self.filter_by_not_between(int(minimum), int(maximum))

        elif filter_method == "first_and_last_digits":
            return self.filter_by_first_and_last_digits()

        elif filter_method == 'odd':
            return self.filter_by_odd()
        elif filter_method == 'even':
            return self.filter_by_even()
        elif filter_method == 'multiple_of':
            return self.filter_by_multiple_of(value)
        elif filter_method == 'no_filtering':
            return self.filter_by_no_filtering()



def fetch(coll , api_key  ,  **kwargs):
    DB_URL = "https://datacube.uxlivinglab.online/db_api/crud/"
    limit = kwargs.get("limit" , 100)
    
    data = {
        "api_key": api_key,
        "operation":"fetch",
        "db_name": "random_table",
        "coll_name": coll,
        "filters": {},
        "limit" : limit,
        "offset" : 0,
        "payment" : False
    }

    response = requests.get(DB_URL, data=data)
    
    if response.status_code != 200:
        if "application/json" in response.headers.get("Content-Type", ""):
            print(response.json())
            raise DatabaseFetchError(response.json().get("message" , "Issue with the database fetch"))
        raise DatabaseFetchError("Issue with the Database Fetch")
    try:
        response_data = json.loads(response.text)
    except Exception as e:
        return None
    result = []
    for rd in response_data['data']:
        for key in rd:
            if key == "_id" or key== "index":
                continue 
            
            result.append(rd[key])
    return result


