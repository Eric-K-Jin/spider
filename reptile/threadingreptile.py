#! /usr/bin/python
#! coding=utf-8

import urllib
import urllib2
import sys
import threading
import time
import chardet
import json
from tools.jsonp import jsonp_to_json
from tools.bankdata import get_bank_data

exitFlag = 0
#多线程执行
class threadingReptile (threading.Thread):
    def __init__(self, bankId, name, url, data, headers, fields, db):
        super(threadingReptile, self).__init__()
        self.bankId = bankId
        self.name = name
        self.url = url
        self.data = data
        self.headers = headers
        self.fields = fields
        self.db = db
    def run(self):
        print "Starting " + self.name

        if self.data != None:
            self.data = urllib.urlencode(self.data)

        response = reptile_data(self.url, self.data, self.headers)

        response = jsonp_to_json(response.strip())

        if response.has_key("Data"):
            response = response["Data"]

        response = get_bank_data(self.bankId, response, self.fields)

        bank_data = self.db[self.bankId].find_one({"name": self.name})

        item = {"PrdList": response}

        if bank_data:
            bank_data = json.loads(bank_data["data"])
            item["PrdList"] += bank_data["PrdList"]
            item["PrdList"] = [dict(t) for t in set([tuple(d.items()) for d in item["PrdList"]])]
            line = json.dumps(dict(item))
            self.db[self.bankId].update({"name": self.name}, {"$set": {"data": line, "time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}})
        else:
            line = json.dumps(dict(item))

            data = {"id": self.bankId,"name": self.name, "data": line, "time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}

            #写进mongodb
            self.db[self.bankId].insert(data)

        print "Exiting " + self.name

#爬虫函数
def reptile_data(url, data, headers):
    request = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e: #捕获异常，主线程退出，程序中止
        print e.code, ' ', e.reason
        sys.exit(0)

    data = response.read()

    charset = chardet.detect(data)["encoding"] #使用chardet模块判断抓取的数据编码再进行转码再编码，防止中文乱码
    return data.decode(charset, 'ignore').encode('utf-8')