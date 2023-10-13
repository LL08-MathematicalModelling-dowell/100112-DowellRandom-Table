import pandas as pd
import requests
import json

DB_URL = "https://datacube.uxlivinglab.online/db_api/crud/"
API_KEY = "wp#!zf&}GPiy06'7'G%3:6]l;].V|<[KIsmlGZCcgm9Enx664fi1psHbJWBM1FZK"


class SearchEngine:
    def __init__(self):

        self.df = None

    def fetch_by_regex(self , column, regex , size, position):
        if not position:
            position = 1

        dfs = []
        for i in range(position, position+size):
            data = fetch('collection_'+str(i))
            if not data:
                continue
            df_temp = pd.DataFrame(data).astype(str)

            dfs.append(df_temp)

        self.df = pd.concat(dfs)

        return self.df[self.df[column].str.contains(regex, regex= True, na=False)]



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

    return response_data['data']
