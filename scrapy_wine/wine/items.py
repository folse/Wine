# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WineItem(Item):

    product_id = Field()
    product_name = Field()
    sales_start_date = Field()
    alcohol = Field()
    color = Field()
    fragrance = Field()
    ingredient = Field()
    sugar = Field()
    producer = Field()
    supplier = Field()
