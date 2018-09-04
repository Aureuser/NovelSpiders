import pymongo
from Novels.setting import MONGO_PORT,MONGO_HOST

class MongoClient():
    def __init__(self):
        self.myclient = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.mydb = self.myclient['test']
        self.mycol = self.mydb["novel"]

    def insert_one(self,data):
        self.mycol.insert_one(data)