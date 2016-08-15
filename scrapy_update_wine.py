#!/usr/bin/python 
#coding=utf-8
import os
import psycopg2

import sys  
reload(sys)
sys.setdefaultencoding('utf8')   

def update_wine_info(index_id):
	cursor.execute("SELECT * FROM wine WHERE id = %s", (index_id,))
	row = cursor.fetchone()
	if row != None:	
		print 'http://www.systembolaget.se' + row[10]
		print os.system("scrapy crawl wine -a url='http://www.systembolaget.se'" + row[10])

if __name__ == '__main__':

	os.chdir("scrapy_wine")

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM wine")
	rows_count = cursor.fetchone()[0]

	for i in xrange(1,rows_count+1):
		update_wine_info(i)
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

	cursor.close()
	conn.close()
