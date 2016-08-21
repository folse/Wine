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

inventory_file_name = 'inventory_%s.xls' % time.strftime('%Y-%m-%d',time.localtime(time.time()))

def write_30days_period(wine_id,store_id,read_sheet):
	for i in xrange(1,31):
		j = 3
		while (j > 0):
			day_period = get_day(i) + '-' +str(j)
			j-=1
			column = (i-1)*3+(3-j)

			cursor.execute("select inventory from inventory where wine_id = %s and store_id = %s and day_period = %s", (wine_id, store_id, day_period))
			result = cursor.fetchone()
			if result != None:
				inventory = result[0]
				sheet.write(read_sheet.nrows,1+column,inventory)

def get_last_day_period():

	return get_day(1) + '-3'

def get_day(fix_day):

	now_time = datetime.datetime.now()
	last_time = now_time + datetime.timedelta(days=-fix_day)

	day_string = last_time.strftime('%Y-%m-%d')

	return day_string

def remove_old_file():
	if os.path.isfile(inventory_file_name): 
		os.remove(inventory_file_name)

def write_30days_title(read_sheet):
	hour_period_array = ['10:00', '14:00', '22:00']
	for i in xrange(1,31):
		j = 3
		while (j > 0):
			j-=1
			day_period = get_day(i)[5:] + ' ' + hour_period_array[j]
			column = (i-1)*3+(3-j)

			sheet.write(read_sheet.nrows+2,1+column,day_period)

if __name__ == '__main__':

	remove_old_file()

	wine_subcategory = u'Rött vin'

	global sheet

	book = Workbook(encoding = 'utf-8')
	sheet = book.add_sheet(wine_subcategory)
	book.save(inventory_file_name)

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

			read_book = xlrd.open_workbook(inventory_file_name)
			read_sheet = read_book.sheet_by_index(0)
			sheet.write(read_sheet.nrows,0,'')
			sheet.write(read_sheet.nrows+1,0,store_info)
			sheet.write(read_sheet.nrows+2,0,'Product Name')
			sheet.write(read_sheet.nrows+2,1,'Product Id')
			write_30days_title(read_sheet)
			book.save(inventory_file_name)

			cursor.execute("select * from inventory where store_id = %s and day_period = %s", (store_id, get_last_day_period()))
			wine_array = cursor.fetchall()

			for i in range(len(wine_array)):

				wine = wine_array[i]
				wine_id = wine[1]
				wine_name = wine[6]
				wine_number = wine[7]

				read_book = xlrd.open_workbook(inventory_file_name)
				read_sheet = read_book.sheet_by_index(0)
				sheet.write(read_sheet.nrows,0,wine_name)
				sheet.write(read_sheet.nrows,1,wine_number)

				write_30days_period(wine_id, store_id, read_sheet)

				book.save(inventory_file_name)
	
	cursor.close()
	conn.close()


