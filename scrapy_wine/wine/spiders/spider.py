
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

        # print response.xpath(/p'//div[@class="details-list"]/ul/li/p').extract()

        ingredient_string = ''

        p_node_string = response.xpath('(//div[@class="details-list"]/ul/li/p)[5]').extract()[0]

        p_text_array = response.xpath('(//div[@class="details-list"]/ul/li/p)[5]/text()').extract()

        p_button_array = response.xpath('(//div[@class="details-list"]/ul/li/p)[5]/button/text()').extract()
        
        new_p_button_array = []

        for i in range(len(p_button_array)):
            if len(p_button_array[i].strip()) > 0:
                new_p_button_array.append(p_button_array[i].strip())

        longest_text_array_length = 0

        if len(p_text_array) > len(new_p_button_array):
            longest_text_array_length = len(p_text_array)
        else:
            longest_text_array_length = len(new_p_button_array)


        if p_node_string[3:10] == '<button':
            print 'Yes!'

            for i in range(longest_text_array_length):

                p_text_item = ''
                button_text_item = ''

                if i < len(p_text_array):
                    p_text_item = p_text_array[i]

                if i < len(new_p_button_array):
                    button_text_item = new_p_button_array[i]

                ingredient_string = ingredient_string + button_text_item + p_text_item

        else:

            for i in range(longest_text_array_length):

                p_text_item = ''
                button_text_item = ''

                if i < len(p_text_array):
                    p_text_item = p_text_array[i]

                if i < len(new_p_button_array):
                    button_text_item = new_p_button_array[i]

                ingredient_string = ingredient_string + p_text_item + button_text_item 

            print 'No!'

        item = WineItem()

        item['sales_start'] = response.xpath('(//div[@class="details-list"]/ul/li)[1]/p/text()').extract()[0]
        item['alcohol'] = response.xpath('(//div[@class="details-list"]/ul/li)[2]/p/text()').extract()[0]
        item['color'] = response.xpath('(//div[@class="details-list"]/ul/li)[3]/p/text()').extract()[0]
        item['fragrance'] = response.xpath('(//div[@class="details-list"]/ul/li)[4]/p/text()').extract()[0]
        item['ingredient'] = ingredient_string
        item['sugar'] = response.xpath('(//div[@class="details-list"]/ul/li)[6]/p/text()').extract()[0]
        item['producer'] = response.xpath('(//div[@class="details-list"]/ul/li)[7]/p/text()').extract()[0]
        item['supplier'] = response.xpath('(//div[@class="details-list"]/ul/li)[8]/p/text()').extract()[0]


        number = self.start_urls[0].split('-')[len(self.start_urls[0].split('-'))-1]

        print number

        item['number'] = number

        yield item
