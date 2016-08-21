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

wine_file_name = 'wine_%s.xls' % time.strftime('%Y-%m-%d',time.localtime(time.time()))

def remove_old_file():
	if os.path.isfile(wine_file_name): 
		os.remove(wine_file_name)

def get_last_day_period():

	return get_day(1) + '-3'

def get_day(fix_day):

	now_time = datetime.datetime.now()
	last_time = now_time + datetime.timedelta(days=-fix_day)

	day_string = last_time.strftime('%Y-%m-%d')

	return day_string

if __name__ == '__main__':

	remove_old_file()

	wine_subcategory = u'Rött vin'

	update_time_period = get_last_day_period()

	book = Workbook(encoding = 'utf-8')
	sheet = book.add_sheet(wine_subcategory)
	book.save(wine_file_name)

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select * from store")
	store_array = cursor.fetchall()
	for i in range(len(store_array)):

		store = store_array[i]

		if store != None:

			store_id = str(store[0])
			store_name = str(store[1])

			store_info = 'Store Id: ' + store_id + ', Store Name: ' + store_name

			print store_id

			read_book = xlrd.open_workbook(wine_file_name)
			read_sheet = read_book.sheet_by_index(0)
			sheet.write(read_sheet.nrows,0,'')
			sheet.write(read_sheet.nrows+1,0,store_info)
			sheet.write(read_sheet.nrows+2,0,'Product Name')
			sheet.write(read_sheet.nrows+2,1,'Product Id')
			sheet.write(read_sheet.nrows+2,2,'Säljstart')
			sheet.write(read_sheet.nrows+2,3,'Alkoholhalt')
			sheet.write(read_sheet.nrows+2,4,'Färg')
			sheet.write(read_sheet.nrows+2,5,'Doft')
			sheet.write(read_sheet.nrows+2,6,'Råvaror')
			sheet.write(read_sheet.nrows+2,7,'Sockerhalt')
			sheet.write(read_sheet.nrows+2,8,'Producent')
			sheet.write(read_sheet.nrows+2,9,'Leverantör')
			book.save(wine_file_name)

			cursor.execute("select wine_id from inventory where store_id = %s and day_period = %s", (store_id, update_time_period))
			wine_id_array = cursor.fetchall()
			for i in range(len(wine_id_array)):

				wine_id = wine_id_array[i]
				cursor.execute("select * from wine where id = %s", wine_id)
				wine = cursor.fetchone()

				read_book = xlrd.open_workbook(wine_file_name)
				read_sheet = read_book.sheet_by_index(0)
				sheet.write(read_sheet.nrows,0,wine[1])
				sheet.write(read_sheet.nrows,1,wine[11])
				sheet.write(read_sheet.nrows,2,wine[2])
				sheet.write(read_sheet.nrows,3,wine[3])
				sheet.write(read_sheet.nrows,4,wine[4])
				sheet.write(read_sheet.nrows,5,wine[5])
				sheet.write(read_sheet.nrows,6,wine[6])
				sheet.write(read_sheet.nrows,7,wine[7])
				sheet.write(read_sheet.nrows,8,wine[8])
				sheet.write(read_sheet.nrows,9,wine[9])
				book.save(wine_file_name)
	
	cursor.close()
	conn.close()


