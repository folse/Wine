
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

        wine_item = WineItem()

        store_array = response.xpath('//ButikOmbud')

        for store in store_array:

            store_id = store.xpath('Nr/text()').extract()[0]

            if not '-' in store_id:

                store_name = ' '
                store_address = ''

                if len(store.xpath('Namn/text()').extract()) > 0:
                    store_name = store.xpath('Namn/text()').extract()[0]

                # if len(store.xpath('Address1/text()').extract()) > 0:
                #     store_address += store.xpath('Address1/text()').extract()[0]

                # if len(store.xpath('Address3/text()').extract()) > 0:
                #     store_address += ',' + store.xpath('Address3/text()').extract()[0]

                if len(store.xpath('Address4/text()').extract()) > 0:
                    store_address += '' + store.xpath('Address4/text()').extract()[0]

                print store_id+","+store_name+","+store_address+'&'

        yield wine_item
            
