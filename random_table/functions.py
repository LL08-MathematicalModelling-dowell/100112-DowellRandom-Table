import pandas as pd
import math  

DB_URL = "https://datacube.uxlivinglab.online/db_api/crud/"
API_KEY = "wp#!zf&}GPiy06'7'G%3:6]l;].V|<[KIsmlGZCcgm9Enx664fi1psHbJWBM1FZK"
import requests
import json

from .utils import extract_digits

column = "column"
class SearchEngine:
    def __init__(self, size, position):
        self.df = None
        required_collection = math.ceil(size/10000)
        if not position:
            position = 1

        dfs = []
        for i in range(position, position+required_collection):
            data = fetch('collection_'+str(i))
            if not data:
                continue
            dfs = dfs + data

        self.df = pd.Series(dfs[:size])


    def fetch_by_regex(self, regex):
        df = self.df[self.df.astype(str).str.contains(regex, regex= True, na=False)]
        return df
    
    def filter_by_contains(self, value):
        df =  self.df[self.df.astype(str).str.contains(value, regex= False, na=False)]
        return df
    
    def filter_by_not_contains(self, value):
        df = self.df[self.df.astype(str).str.contains(value, regex= False, na=False)]
        return df
    
    def filter_by_exact(self, value):
       pass
    
    def filter_by_starts_with(self, value):
        df = self.df[self.df.astype(str).str.startswith(value, na=False)]
        return df
    
    def filter_by_ends_with(self, value):
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
        df = self.df[self.df%value==0]
        return df

    def filter_by_no_filtering(self):
        return self.df

    def filter_by_first_and_last_digits(self):
        self.df = self.df.apply(extract_digits)
        return self.df

    def filter_by_method(self, filter_method , value, minimum=None, maximum=None):
        print(minimum, maximum)
        if filter_method == 'regex':
            return self.fetch_by_regex(value)
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
        elif filter_method == 'in_between':
            return self.filter_by_between(int(minimum), int(maximum))
        elif filter_method == 'not_in_between':
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



def fetch(coll):
    data = {
        "api_key": API_KEY,
        "operation":"fetch",
        "db_name": "random_table",
        "coll_name": coll,
        "filters": {}
    }


    response = requests.get(DB_URL, data=data)
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


