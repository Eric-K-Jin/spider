#! coding=utf-8

import pymongo

class MongoDbClient:

    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host, port)
        self.db = {}

    def connectDb(self, dbname):
        self.db = self.client[dbname]
        return self.db #返回对应数据库的资源句柄