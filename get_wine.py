#!/usr/bin/python 
#coding=utf-8
import os
import json
import time
import urllib
import urllib2
from xlwt import Workbook
import xlrd
import psycopg2

import sys  
reload(sys)

sys.setdefaultencoding('utf8')   
sys.setrecursionlimit(1000000)

def get_store_wine(wine_subcategory,store_id,page):

	request_data = urllib.urlencode({'subcategory':wine_subcategory,'sortdirection':'Ascending','site':store_id,'fullassortment':'0','page':page}) 

	request_url = 'http://www.systembolaget.se/api/productsearch/search?' + request_data.replace('+','%20')

	print str(store_id) + ',' + str(page)

	try:
		resp = urllib2.urlopen(request_url).read()
	except Exception, e:
		print e
		time.sleep(60)
		resp = urllib2.urlopen(request_url).read()
	  
	resp_json = json.loads(resp)
	meta_data = resp_json['Metadata']
	product_array = resp_json['ProductSearchResults']

	for i in range(len(product_array)):
		
		product = product_array[i]

		global product_id
		product_id = product['ProductId']
		product_name = str(product['ProductNameBold']).encode("utf-8") + ' ' + str(product['ProductNameThin']).encode("utf-8")
		product_number = product['ProductNumber']
		product_inventory = product['QuantityText']
		product_url = product['ProductUrl']

		cursor.execute("SELECT * FROM wine WHERE sys_wine_id = %s", (product_id,))
		result = cursor.fetchone()
		if result == None:
			cursor.execute("INSERT INTO wine(sys_wine_id, name, number, url) VALUES (%s, %s, %s, %s)", (product_id, product_name, product_number, product_url))
    		conn.commit()

    	cursor.execute("SELECT * FROM store_wine WHERE sys_wine_id = %s and sys_store_id = %s", (product_id, store_id))
    	result = cursor.fetchone()
    	if result == None:
			cursor.execute("INSERT INTO store_wine(sys_wine_id, sys_store_id, inventory)VALUES(%s, %s, %s)", (product_id, store_id, product_inventory))
			conn.commit()

	# global store_index
	next_page = meta_data['NextPage']
	if next_page > 0:
		print 'next_page > 0'
		get_store_wine(wine_subcategory,store_id,next_page)

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()

	wine_subcategory = u'Rött vin'

	cursor.execute("select max(id) from store")
	result = cursor.fetchone()
	for i in xrange(1,result[0]+1):
		exist = cursor.execute("select * from store where id = %s", [i])
		result = cursor.fetchone()
		if result != None:
			print "////////////////////////  " + result[1]
			get_store_wine(wine_subcategory,result[1],0)

	cursor.close()
	conn.close()
