#!/usr/bin/python 
#coding=utf-8
import os
import json
import time
import datetime
import urllib
import urllib2
from xlwt import Workbook
import xlrd
import psycopg2

import sys  
reload(sys)

sys.setdefaultencoding('utf8')   
sys.setrecursionlimit(1000000)

def get_store_wine(wine_subcategory,store_id,sys_store_id,page):

	request_data = urllib.urlencode({'subcategory':wine_subcategory,'sortdirection':'Ascending','site':sys_store_id,'fullassortment':'0','page':page}) 

	request_url = 'http://www.systembolaget.se/api/productsearch/search?' + request_data.replace('+','%20')

	print 'store: ' + str(store_id) + ', page:' + str(page)

	try:
		resp = urllib2.urlopen(request_url).read()
	except Exception, e:
		print e
		time.sleep(60)
		resp = urllib2.urlopen(request_url).read()
	  
	resp_json = json.loads(resp)
	meta_data = resp_json['Metadata']
	product_array = resp_json['ProductSearchResults']

	count = 0
	while (count < len(product_array)):
		product = product_array[count]
		save_wine_info(product, store_id)
		count = count + 1

	next_page = meta_data['NextPage']
	if next_page > 0:
		get_store_wine(wine_subcategory,store_id,sys_store_id,next_page)

def save_wine_info(product, store_id):
    sys_wine_id = product['ProductId']
    wine_name = str(product['ProductNameBold']).encode("utf-8")

    if product['ProductNameThin'] != None:
    	wine_name = wine_name + ' ' + str(product['ProductNameThin']).encode("utf-8")

    wine_number = product['ProductNumber']
    wine_inventory = product['QuantityText'][:-3]
    wine_url = product['ProductUrl']
    wine_id = 0

    cursor.execute("SELECT * FROM wine WHERE sys_wine_id = %s", (sys_wine_id,))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO wine(sys_wine_id, name, number, url) VALUES (%s, %s, %s, %s) RETURNING id", (sys_wine_id, wine_name, wine_number, wine_url))
        conn.commit()
        wine_id = cursor.fetchone()[0]
        print 'Inserted a new wine'
    else:
        wine_id = result[0]

    print wine_id

    cursor.execute("INSERT INTO inventory(wine_id, wine_name, wine_number, store_id, inventory, day_period, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)", (wine_id, wine_name, wine_number, store_id, wine_inventory, update_time_period, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()

def get_update_time_period():

	current_day_string = datetime.datetime.now().strftime('%Y-%m-%d')
	current_hour_string = datetime.datetime.now().strftime('%H')

	if current_hour_string[0] == '0':
		current_hour_string = current_hour_string[1]

	current_hour = int(current_hour_string)

	if current_hour < 10:
		return current_day_string + '-1'
	elif current_hour < 14:
		return current_day_string + '-2'
	elif current_hour < 22:
		return current_day_string + '-3'

	return current_day_string

if __name__ == '__main__':

	wine_subcategory = u'Rött vin'

	global update_time_period
	update_time_period = get_update_time_period()
	print update_time_period

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()

	cursor.execute("SELECT COUNT(*) FROM store")
	result = cursor.fetchone()
	for i in range(result[0]):
		exist = cursor.execute("SELECT * FROM store WHERE id = %s", [i+1])
		result = cursor.fetchone()
		if result != None:
			print "//////////  " + result[1] + " " + result[3]
			get_store_wine(wine_subcategory, i+1, result[3], 0)

	cursor.close()
	conn.close()
