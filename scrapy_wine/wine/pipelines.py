# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class WinePipeline(object):
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize,signals.engine_started)
        dispatcher.connect(self.finalize,signals.engine_stopped)

    def process_item(self,item,spider):
        print item
        cursor = self.conn.cursor()
    	exist = cursor.execute("SELECT * FROM wine WHERE number = %s", (item['number'],))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE wine SET(sales_start, alcohol, color, fragrance, ingredient, sugar, producer, supplier) = (%s,%s,%s,%s,%s,%s,%s,%s) WHERE number = %s", (item['sales_start'], item['alcohol'], item['color'], item['fragrance'], item['ingredient'], item['sugar'], item['producer'], item['supplier'], item['number']))
        else:
            print "Update Faild: can't find the wine."
        return item

    def initialize(self):
        self.conn = psycopg2.connect(database="wine", user="folse", password="", host="localhost", port="5432")

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn=None
