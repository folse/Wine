
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request

from wine.items import WineItem

class WineSpider(Spider):
    name = "wine"
    allowed_domains = ["localhost"]
    # start_urls = ["http://localhost:8000/Desktop/question.html"]

    def __init__(self, url=None):
        self.start_urls = ['%s' % url]

    def start_requests(self):  
        for url in self.start_urls:
            #yield Request(url, cookies={'login_token':'2|1:0|10:1434072495|11:login_token|44:ODU4ZWYzNmI5ODQyNDdkMzg3ODJiOTg5MGE5NWQ1MTQ=|b4644f5ecf993fcdb088215742092e49df31c96d89f58b034376feb0a1862637','user':'2|1:0|10:1434072495|4:user|164:eyJ1c2VybmFtZSI6ICJcdTVmNjJcdTVmNjIiLCAibG9naW5fc24iOiAiNFhZTEFPbXA4cnU5VXhZWCIsICJsb2dpbl90b2tlbiI6ICI4NThlZjM2Yjk4NDI0N2QzODc4MmI5ODkwYTk1ZDUxNCIsICJyb2xlIjogMX0=|61777a2781e6c9cac8a8ffec125ebf2398d9bf09b64d453deb2337379878176d'})
            yield Request(url)

    def parse(self, response):

        # print response.body

        print response.xpath('//div[@class="details-list"]/ul/li/p/button/text()').extract()[0].strip()

        item = WineItem()

        info_array = response.xpath('//div[@class="details-list"]/ul/li/p/text()').extract()

        item['sales_start'] = info_array[0]
        item['alcohol'] = info_array[1]
        item['color'] = info_array[2]
        item['fragrance'] = info_array[3]
        item['ingredient'] = response.xpath('//div[@class="details-list"]/ul/li/p/button/text()').extract()[0].strip()
        item['sugar'] = info_array[5]
        item['producer'] = info_array[6]
        item['supplier'] = info_array[7]

        number = self.start_urls[0].split('-')[len(self.start_urls[0].split('-'))-1]

        print number

        item['number'] = number

        yield item
            
