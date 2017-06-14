#! coding=utf-8

import json
from scrapy.http import FormRequest
from scrapy.spiders import Spider
from tutorial.items import BankItem

class SpdbSpider(Spider):
    name = 'spdb'
    allowed_domains = ["spdb.com.cn"]
    #减慢爬取速度为1s/次
    download_delay = 1
    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial.pipelines.BankPipeline': 1
        }
    }

    def start_requests(self):
        url = "http://per.spdb.com.cn/was5/web/search"
        for i in range(1, 3):
            formdata = {
                "page": str(i),
                "metadata": "finance_state|finance_no|finance_allname|finance_anticipate_rate|finance_limittime|finance_lmttime_info|finance_type|docpuburl|finance_ipo_enddate|finance_indi_ipominamnt|finance_indi_applminamnt",
                "channelid": "266906",
                "searchword": "(product_type=3)*finance_limittime = %*(finance_currency = 01)*(finance_state='可购买')"
            }

            yield FormRequest(url, callback=self.parse_model, formdata=formdata)

    def parse_model(self, response):
        jsonBody = json.loads(response.body)
        models = jsonBody['rows']
        bankItem = BankItem()
        items = []
        for dict in models:
            data = {
                "finance_allname": dict["finance_allname"],
                "finance_anticipate_rate": dict["finance_anticipate_rate"],
                "finance_indi_applminamnt": dict["finance_indi_applminamnt"],
                "finance_indi_ipominamnt": dict["finance_indi_ipominamnt"],
                "finance_lmttime_info": dict["finance_lmttime_info"],
                "finance_no": dict["finance_no"]
            }
            items.append(data)
        bankItem['PrdList'] = items
        yield bankItem