#! coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import BankItem

class NjcbSpider(Spider):
    name = 'njcb'
    allowed_domains = ["njcb.com.cn"]
    #减慢爬取速度为1s/次
    download_delay = 1
    start_urls = [
        "http://www.njcb.com.cn/eportal/ui?pageId=301361"
    ]

    def parse(self, response):
        selector = Selector(response)

        #获取要爬取的内容
        item = BankItem()
        PrdList = []
        list = selector.css("#form > table:nth-child(5) > tbody > tr")
        for row in list:
            name = row.xpath("td/div/div[1]/p/a/text()").extract()
            data = {
                'PrdName': name[0],
                'PrdRate': row.xpath("td/div/div[1]/table/tbody/tr/td[3]/p/span/text()").extract()[0],
                'PrdPeriod': row.xpath("td/div/div[1]/table/tbody/tr/td[4]/p/span/text()").extract()[0],
                'PrdTime': row.xpath("td/div/div[1]/table/tbody/tr/td[5]/p[1]/text()").extract()[0],
                'PrdEndTime': row.xpath("td/div/div[1]/table/tbody/tr/td[5]/p[2]/text()").extract()[0],
                'PrdType': row.xpath("td/div/div[1]/table/tbody/tr/td[2]/p[1]/span/text()").extract()[0]
            }

            PrdList.append(data)


        item['PrdList'] = PrdList

        yield item

        #下一页
        nextPage = selector.xpath('//*[@id="pagingDiv"]/table/tbody/tr/td/a[3]/@href').extract()
        if len(nextPage) > 0:
            currentPage = int(selector.css('#currentPage::attr(value)').extract()[0]) + 1
            nextUrl = "".join((self.start_urls[0], "&currentPage=", str(currentPage)))
            yield Request(nextUrl, callback=self.parse)