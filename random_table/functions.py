import pandas as pd

class SearchEngine:
    def __init__(self):
        self.df = pd.read_json("/home/uxlivinglab200112/100112-DowellRandom-Table/random-data-files/data1.json").astype(str)

    def fetch_by_regex(self , column, regex , size):
        df = self.df[self.df[column].str.contains(regex, regex= True, na=False)]
        return df.head(size)

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