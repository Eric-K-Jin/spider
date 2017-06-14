#!coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import BankItem

class XmccbSpider(Spider):
    name = 'xmccb'
    allowed_domains = ["xmccb.com"]
    # 减慢爬取速度为1s/次
    download_delay = 1
    start_urls = [
        "http://www.xmccb.com/searchLicai.jspx?scId=1197&cId=1197&q="
    ]

    def parse(self, response):
        sel = Selector(response)
        list = sel.css("#mark > table > tr")
        item = BankItem()
        PrdList = []
        for row in list:
            name = row.xpath("td[1]/a/text()").extract()
            if len(name) > 0:
                data = {
                    'name': name[0],
                    'rate': row.xpath("td[2]/text()").extract()[0],
                    'period': row.xpath("td[3]/text()").extract()[0],
                    'time': row.xpath("td[4]/text()").extract()[0],
                    'endTime': row.xpath("td[5]/text()").extract()[0],
                    'type': row.xpath("td[6]/text()").extract()[0],
                }

                PrdList.append(data)
        item['PrdList'] = PrdList
        yield item

        # 下一页连接
        pageDiv = sel.css(".Page > div")
        nextPage = pageDiv.xpath('a[@class="Page_Next"]/@href').extract()[0]
        if nextPage:
            nextUrl = "http://www.xmccb.com/" + nextPage
            yield Request(nextUrl, callback=self.parse)