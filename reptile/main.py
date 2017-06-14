#! /usr/bin/python
#! coding=utf-8

import threadingreptile
from conf.conf import get_bank_url
from conf.mongodb import MongoDbClient

#创建mongodb连接对象
connection = MongoDbClient('localhost', 27017)

#获取数据库实例
db = connection.connectDb('reptilebank')

#多线程并发执行爬虫并入库 TODO:mongodb操作
urls = get_bank_url()

for key, value in urls.items():
    myThread = threadingreptile.threadingReptile(key, value['name'], value['url'], value['values'], value['headers'], value['fields'], db)
    myThread.start()