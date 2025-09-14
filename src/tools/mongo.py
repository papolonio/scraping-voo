import os
import pandas
from pymongo import MongoClient

class MongoConnection:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
            cls._instance._db - None
            cls._instance._collection = None
        return cls._instance


    def __init__(self, host='localhost', port=27017, database='test', collection='data'):
        if self.client is None: 
            self.host = os.getenv('MONGO_HOST', host)
            self.port = os.getenv('MONGO_PORT', port)
            self.database = os.getenv('MONGO_DATABASE', database)
            self.collection = os.getenv('MONGO_COLLECTION', collection)
            self.connect()

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self._db = self._client(self.database_name)
        self._collection = self._db(self.collection)

    def save_dataframe(self,df):
        data = df.to_dict(orient='records')
        try:
            self.collection.insert_many(data)
        except:
            print(f"Error inserting data")

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")