#! /usr/bin/python
#! coding=utf-8

from pymongo import MongoClient

class MongoDbClient:
    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = {}

    def connectDb(self, dbname):
        self.db = self.client[dbname]
        return self.db  #返回对应数据库的资源句柄
