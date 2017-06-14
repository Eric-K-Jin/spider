# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import itertools
from tools.mongodb import MongoDbClient
from scrapy.conf import settings

db = MongoDbClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']).connectDb(settings['MONGODB_DB'])

class BankPipeline(object):
    def process_item(self, item, spider):
        banks = settings['BANK_INFO']
        bank_name = banks[spider.name]
        bank_data = db[spider.name].find_one({"name": bank_name})
        if bank_data:
            bank_data = json.loads(bank_data["data"])
            item["PrdList"] += bank_data["PrdList"]
            #这里的写法是先创建一个set集合和一个list列表，遍历PrdList的元组数组，并塞进set集合中，通过判断set集合是否存在相同的元组数组来进行去重，如下代码
            '''
            l = [{'a': 123, 'b': 1234},
                    {'a': 3222, 'b': 1234},
                    {'a': 123, 'b': 1234}]
            
            seen = set()
            new_l = []
            for d in l:
                t = tuple(d.items())
                if t not in seen:
                    seen.add(t)
                    new_l.append(d)
            
            print new_l 
            输出：[{'a': 123, 'b': 1234}, {'a': 3222, 'b': 1234}]
            '''
            item["PrdList"] = [dict(t) for t in set([tuple(d.items()) for d in item["PrdList"]])]
            line = json.dumps(dict(item))
            db[spider.name].update({"id": spider.name}, {"$set": {"name": bank_name, "data": line, "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}})
        else:
            line = json.dumps(dict(item))
            data = {
                "id": spider.name,
                "name": bank_name,
                "data": line,
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            }
            db[spider.name].insert(data)
        pass