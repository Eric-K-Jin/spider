#! coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import BankItem

class GdnybankSpider(Spider):
    name = 'gdnybank'
    allowed_domains = ["gdnybank.com"]
    #减慢爬取速度为1s/次
    download_delay = 1
    start_urls = [
        "http://www.gdnybank.com/grlccs/index.html#mao_c"
    ]

    def parse(self, response):
        selector = Selector(response)

        #获取要爬取的内容
        item = BankItem()
        list = selector.css(".table > table > tr")
        PrdList = []

        for row in list:
            name = row.xpath("td[1]/a/text()").extract()
            if len(name) > 0:
                data = {
                    "PrdName": name,
                    "PrdCode": row.xpath("td[2]/text()").extract(),
                    "PrdPeriod": row.xpath("td[3]/text()").extract(),
                    "PrdRaisingPeriod": row.xpath("td[4]/text()").extract(),
                    "PrdExpirePeriod": row.xpath("td[5]/text()").extract(),
                    "PrdType": row.xpath("td[6]/text()").extract(),
                    "PrdApr": row.xpath("td[7]/text()").extract()
                }

                for key, value in data.items():
                    if len(value) == 0:
                        data[key] = "0"
                    else:
                        data[key] = value[0]

                PrdList.append(data)

        item['PrdList'] = PrdList

        yield item

        #下一页
        pageDiv = selector.css(".pages_prod > a")
        num = len(pageDiv)
        nextPage = selector.xpath("//div[@class='Pages pages_prod']/a["+str(num)+"]/@href").extract()[0]
        if nextPage:
            nextUrl = "".join(("http://www.", self.allowed_domains[0], nextPage))
            yield Request(nextUrl, callback=self.parse)