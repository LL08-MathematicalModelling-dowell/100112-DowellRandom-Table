import pandas as pd

class SearchEngine:
    def __init__(self):
        self.df = pd.read_json("random-data-files/data1.json").astype(str)

    def fetch_by_regex(self , column, regex , size):
        df = self.df[self.df[column].str.contains(regex, regex= True, na=False)]
        return df.head(size)
    
    def filter_by_contains(self , column, value , size):
        df = self.df[self.df[column].str.contains(value, regex= False, na=False)]
        return df.head(size)
    
    def filter_by_not_contains(self , column, value , size):
        df = self.df[~self.df[column].str.contains(value, regex= False, na=False)]
        return df.head(size)
    
    def filter_by_exact(self , column, value , size):
        df = self.df[self.df[column] == value]
        return df.head(size)
    
    def filter_by_starts_with(self , column, value , size):
        df = self.df[self.df[column].str.startswith(value, na=False)]
        return df.head(size)
    
    def filter_by_ends_with(self , column, value , size):
        df = self.df[self.df[column].str.endswith(value, na=False)]
        return df.head(size)
    
    def filter_by_greater_than(self , column, value , size):
        df = self.df[self.df[column] > value]
        return df.head(size)
    
    def filter_by_less_than(self , column, value , size):
        df = self.df[self.df[column] < value]
        return df.head(size)
    
    def filter_by_between(self , column, value , size):
        df = self.df[(self.df[column] > value[0]) & (self.df[column] < value[1])]
        return df.head(size)
    
    def filter_by_not_between(self , column, value , size):
        df = self.df[~((self.df[column] > value[0]) & (self.df[column] < value[1]))]
        return df.head(size)
    
    def fetch_by_filter(self , column, filter_method , value , position):
        if filter_method == 'regex':
            return self.fetch_by_regex(column, value, position)
        elif filter_method == 'contains':
            return self.filter_by_contains(column, value, position)
        elif filter_method == 'not_contains':
            return self.filter_by_not_contains(column, value, position)
        elif filter_method == 'exact':
            return self.filter_by_exact(column, value, position)
        elif filter_method == 'starts_with':
            return self.filter_by_starts_with(column, value, position)
        elif filter_method == 'ends_with':
            return self.filter_by_ends_with(column, value, position)
        elif filter_method == 'greater_than':
            return self.filter_by_greater_than(column, value, position)
        elif filter_method == 'less_than':
            return self.filter_by_less_than(column, value, position)
        elif filter_method == 'between':
            return self.filter_by_between(column, value, position)
        elif filter_method == 'not_between':
            return self.filter_by_not_between(column, value, position)

class SearchManager:
    __instance = None

    def __init__(self ):
        if SearchManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
           SearchManager.__instance = SearchEngine()

    @staticmethod
    def getInstance():
        if SearchManager.__instance == None:
            SearchManager()
        return SearchManager.__instance