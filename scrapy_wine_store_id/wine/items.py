# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WineItem(Item):

    store_id = Field()
    store_name = Field()
    store_address = Field()

