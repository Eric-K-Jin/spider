#! coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import BankItem

class NbcbSpider(Spider):
    name = 'nbcb'
    allowed_domains = ["nbcb.com.cn"]
    #减慢爬取速度为1s/次
    download_delay = 1
    start_urls = [
        "http://www.nbcb.com.cn/wealth_management_center/financial/"
    ]

    def parse(self, response):
        selector = Selector(response)

        #获取要爬取的内容
        item = BankItem()
        list = selector.xpath("//table[@id='tbl_wealth_saling']/tbody[1]/tr")
        PrdList = []
        i = 1

        for row in list:

            data = {
                "PrdCode": row.xpath("td[1]/text()").extract(),
                "PrdName": row.xpath("td[2]/a/text()").extract(),
                "PrdPeriod": row.xpath("td[3]/text()").extract(),
                "PrdApr": row.xpath("td[4]/text()").extract(),
                "PrdStartReleasePeriod": row.xpath("td[5]/div[1]/text()").extract(),
                "PrdEndReleasePeriod": row.xpath("td[5]/div[2]/text()").extract()
            }

            for key, value in data.items():
                if len(value) == 0:
                    data[key] = "0"
                else:
                    data[key] = value[0]

            PrdList.append(data)
            i += 1

        item['PrdList'] = PrdList

        yield item

        print "进入下一次爬虫"

        pageNum = 2

        while(pageNum <= 25):
            url = "".join((self.start_urls[0], "index_", str(pageNum), ".shtml"))
            yield Request(url, callback=self.parse)
            pageNum += 1