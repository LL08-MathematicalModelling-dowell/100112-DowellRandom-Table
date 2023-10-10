from pyspark.sql import SparkSession

class SparkSes():
    def __init__(self, jsonfile):
        self.spark = SparkSession.builder \
            .appName("YourAppName") \
            .config("spark.executor.cores", "4")\
            .config("spark.executor.memory", "4g")\
            .config("spark.driver.memory", "2g")\
            .getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
        
        try:
            self.df = self.spark.read.json(jsonfile)
            self.df.cache() 
        except Exception as e:
            raise Exception("Error while reading json file" + str(e))

    def search_by_regex(self, column, regex , size):
        try:
            df = self.df.where(self.df[column].rlike(regex))
            return df.limit(size)
        except Exception as e:
            raise Exception("Error while searching by regex" + str(e))
