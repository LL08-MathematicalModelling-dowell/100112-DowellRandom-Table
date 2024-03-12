import pandas as pd
import math  
import requests
import json
import concurrent.futures 
import time

from django.conf import settings

from .utils import extract_digits , check_value_integer_string
from .exceptions import DatabaseFetchError , RandomTableTypeError ,RandomTableFilteringError


column = "column"
class SearchEngine:
    """
    A class that
    """
    
    error_messages = {
        "regex" : lambda value : f"Regex value {value} yields an empty result",
       "contains" : lambda value : f"Contain value {value} yields an empty result",
       "not_contains" : lambda value : f"Not Contain value {value} yields an empty result",
       "exact" : lambda value : f"Exact value {value} can't be found",
       "starts_with" : lambda value : f"Can't find values that start with {value} ",
       "ends_with" : lambda value : f"Can't find values that ends with {value}",
       "greater_than" : lambda value : f"Can't find values that are greater than {value}",
       "less_than" : lambda value : f"Can't find values less than {value}",
       "betweens" : lambda mini , maxi : f"Can't find values that are between {mini} and {maxi}",
       "not_betweens" : lambda mini , maxi : f"Can't find values that are not between {mini} and {maxi}"}
    
    
    
    def __init__(self, size, position , set_size ,   filter_method , api_key= None  , pagination = True, **kwargs):
        self.df = None
        if not position:
            position = 1

    
        if not pagination:
            self.total_filtered_data = self._processor_without_pagination(size , position , set_size , 
                                                                          filter_method , api_key = api_key, **kwargs)
        else:
            self.total_filtered_data = self._processor_with_pagination(size , position , filter_method , api_key,
                                                                       **kwargs)
            
        
        if self.total_filtered_data.empty:
            if filter_method.endswith("betweens"):
                self.handle_filtering_error(self.error_messages[filter_method](kwargs.get("minimum") , kwargs.get("maximum")))
            else:
                self.handle_filtering_error(self.error_messages[filter_method](kwargs.get("value")))
        self.total_filtered_data = self.total_filtered_data[:size]
            
            
    def _processor_with_pagination(self , size , position , filter_method ,  api_key , **kwargs):
        df = None
        required_collection = math.ceil(size/10000)
        if not position:
            position = 1

        dfs = []
        for i in range(position, position+required_collection):
            data = fetch_data('collection_'+str(i) , api_key , limit = size , **kwargs)
            if not data:
                continue
            dfs = dfs + data
            
        if not dfs:
            raise DatabaseFetchError("No datafound while for this size")
        self.df = pd.Series(dfs[:size])
        
        return self.filter_by_method(filter_method , **kwargs)
        
        
    def _processor_without_pagination(self, size , position , set_size , filter_method , api_key = None, **kwargs):
        
        total_filtered_data = pd.Series([])
                
        if size < 10000:
            number_of_threads = 1
            
        elif size >= 10000 and size < 100000:
            
            number_of_threads = 2 * math.ceil(size/10000)
            
        else:
            number_of_threads = 5 * math.ceil(size/100000)
            
        
        for i in range(1, 1000 , number_of_threads):
            
            dfs_ = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
                futures = [executor.submit(fetch , 'collection_'+str(i) , api_key , limit = size , **kwargs)\
                                    for i in range(i ,  i + number_of_threads)]
                
            
                for future in concurrent.futures.as_completed(futures):
                    try:
                        dfs = future.result()
                        dfs_.extend(dfs)
                        
                    except KeyboardInterrupt as e:
                        executor.shutdown(wait = True)
                        
                    except Exception as e:
                        pass
                        

            if not dfs_:
                continue
           
            self.df = pd.Series(dfs_)

            filtered_data = self.filter_by_method(filter_method , **kwargs)
            total_filtered_data = pd.concat([total_filtered_data , filtered_data])
            
                
            if total_filtered_data.any():

                if len(total_filtered_data) >= size:
                    break
        
        
        return total_filtered_data[:size]
        
    def handle_filtering_error(self ,  message , df=None):
        if isinstance(df , pd.Series) and df.empty:
            raise RandomTableFilteringError(message)
        raise RandomTableFilteringError(message)
        
        
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
        
        
        df = pd.concat([min_df,max_df])
        
        return df


    def filter_by_odd(self):
        df = self.df[(self.df%2!=0)]
        
        
        return df

    def filter_by_even(self):
        df = self.df[self.df%2==0]
        
        
        return df
    def filter_by_multiple_of(self, value):

        df = self.df[self.df % int(value) ==0]
        
        return df

    def filter_by_no_filtering(self):
        return self.df

    def filter_by_first_and_last_digits(self):
        df = self.df.apply(extract_digits)
        return df
    
    def filter_by_one_digits(self):
        df = self.df.apply(lambda x: [int(i) for i in str(x)])
        return df

    def filter_by_method(self, filter_method , **kwargs):
        
        value = kwargs.get("value")
        minimum = kwargs.get("minimum")
        maximum = kwargs.get("maximum")
        
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
        elif filter_method == "one_digits":
            return self.filter_by_one_digits()
        
        else:
            return self.filter_by_no_filtering()
        
        
def fetch_data(coll , api_key , offset = 0 , limit = 1000 ,  **kwargs):
    DB_URL = "https://datacube.uxlivinglab.online/db_api/crud/"
    
    data = {
        "api_key": api_key,
        "operation":"fetch",
        "db_name": "random_table",
        "coll_name": coll,
        "filters": {},
        "limit" : limit,
        "offset" : offset,
        "payment" : False
    }
    response = requests.get(DB_URL, data=data)
        
    if response.status_code != 200:
            
            if "application/json" in response.headers.get("Content-Type", ""):
                
                raise DatabaseFetchError(response.json().get("message" , "Issue with the database fetch"))
            raise DatabaseFetchError("Issue with the Database Fetch")
        
    try:
            response_data = json.loads(response.text)
    except Exception as e:
            return []
    result = []
    
    start = time.time()
    

    for rd in response_data['data']:
            for key in rd:
                if key == "_id" or key== "index":
                    continue 
                result.append(rd[key])
            
    return result
    



def fetch(coll , api_key  , limit = 1000 , **kwargs):
    
    number_of_rounds = round(1000/limit)

    if limit > 500:
        return fetch_data(coll , api_key , limit = limit , **kwargs)
    
    else:
        
        
        
        
        if number_of_rounds >= 10:
            number_of_rounds = 2

        total_results = []
        
        
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_rounds) as executor:
            futures = [executor.submit(fetch_data , coll , api_key , offset = i , limit = limit) \
                                       for i in range(0 , limit * number_of_rounds , limit)]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    total_results.extend(result)
                    
                except KeyboardInterrupt as e:
                    executor.shutdown(wait = True)
                except Exception as e:
                    pass
                    
        return total_results
            
            
            
    
        


