#! coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import BankItem

class CzcbSpider(Spider):
    name = 'czcb'
    allowed_domains = ["czcb.com.cn"]
    #减慢爬取速度为1s/次
    download_delay = 1
    start_urls = [
        "http://www.czcb.com.cn/gryw/rxlccp/index.shtml"
    ]

    def parse(self, response):
        selector = Selector(response)

        #获取要爬取的内容
        item = BankItem()
        list = selector.css(".personal_jijin_list > table > tr")
        PrdList = []

        for row in list:
            name = row.xpath("td[2]/a/text()").extract()
            if len(name) > 0:
                data = {
                    "PrdCode": row.xpath("td[1]/text()").extract()[0],
                    "PrdName": name[0],
                    "PrdCurrency": row.xpath("td[3]/text()").extract()[0],
                    "PrdApr": row.xpath("td[4]/text()").extract()[0],
                    "PrdRaisingPeriod": row.xpath("td[5]/text()").extract()[0],
                    "PrdStartReleasePeriod": row.xpath("td[6]/text()").extract()[0],
                    "PrdEndReleasePeriod": row.xpath("td[7]/text()").extract()[0],
                    "PrdPeriod": row.xpath("td[8]/text()").extract()[0]
                }

                PrdList.append(data)

        item['PrdList'] = PrdList

        yield item

        #下一页
        nextPage = selector.xpath("//a[@class='page_next']/@href").extract()[0]
        if nextPage:
            nextUrl = "".join(("http://www.", self.allowed_domains[0], nextPage))
            yield Request(nextUrl, callback=self.parse)