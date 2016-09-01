#!/usr/bin/python 
# -*- coding: UTF-8 -*-
import os
import time
import datetime
import xlsxwriter
import psycopg2

import sys  
reload(sys)
sys.setdefaultencoding('utf8')

inventory_file_name = 'inventory_%s.xlsx' % time.strftime('%Y-%m-%d',time.localtime(time.time()))

def remove_old_file():
	if os.path.isfile(inventory_file_name): 
		os.remove(inventory_file_name)

def get_day(start_time, fix_day):

	if start_time == None:
		start_time = datetime.datetime.now()

	last_time = start_time + datetime.timedelta(days=-fix_day)
	day_string = last_time.strftime('%Y-%m-%d')

	return day_string

def write_days_title(row, days_count):

	hour_period_array = ['10:00', '14:00', '22:00']
	for i in xrange(0,days_count+1):
		j = 3
		while (j > 0):
			j-=1
			day_period = get_day(end_day,i)[5:] + ' ' + hour_period_array[j]
			column = i*3+(3-j)+1
			sheet.write(row,column,day_period)

def write_period_inventory(wine_array, store_id, day_period, col):

	row = 2

	inventory_dict = {}

	inventory_table_name = 'inventory' + str(store_id)
	sql = "select * from " + inventory_table_name + " where day_period = '%s'" % day_period

	cursor.execute(sql)
	inventory_array = cursor.fetchall()

	for inventory in inventory_array:

		wine_id = inventory[1]
		wine_inventory = inventory[3]

		inventory_dict[wine_id] = wine_inventory

	for wine in wine_array:

		wine_id = wine[0]
		if inventory_dict.has_key(wine_id):
			sheet.write(row,col,inventory_dict[wine_id])
		else:
			sheet.write(row,col,0)

		row +=1

def write_store_period_wines(store_id):

	global row
	row = row+1

	inventory_table_name = 'inventory' + str(store_id)
	cursor.execute("select DISTINCT wine_id, wine_name, wine_number from " + inventory_table_name + " where day_period between %s and %s ORDER BY wine_id", (start_date, end_date))
	wine_array = cursor.fetchall()

	for wine in wine_array:

		wine_id = str(wine[0])
		wine_name = str(wine[1])
		wine_number = str(wine[2])

		row +=1

		sheet.write(row,0,wine_name)
		sheet.write(row,1,wine_number)

	return wine_array

def write_store(store):

	global row
	global days_count

	store_id = str(store[0])
	store_name = str(store[1])

	# print store_id

	row +=3

	store_info = 'Store Id: ' + store_id + ', Store Name: ' + store_name
	
	sheet.write(row,col,store_info)
	sheet.write(row+1,col,'Product Name')
	sheet.write(row+1,col+1,'Product Id')
	write_days_title(row+1,days_count)

	wine_array = write_store_period_wines(store_id)

	period_array = ['1', '2', '3']
	for i in xrange(0,days_count+1):
		j = 3
		while (j > 0):
			j-=1
			day_period = get_day(end_day,i) + '-' + period_array[j]
			column = i*3+(3-j)+1
			write_period_inventory(wine_array, store_id, day_period, column)


if __name__ == '__main__':

	remove_old_file()

	book = xlsxwriter.Workbook(inventory_file_name)
	sheet = book.add_worksheet()

	row = -3
	col = 0

	start_date = '2016-08-17'
	end_date = '2016-08-22'

	start_day = datetime.datetime.strptime(start_date,'%Y-%m-%d')
	end_day = datetime.datetime.strptime(end_date,'%Y-%m-%d')
	days_count = (end_day-start_day).days

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select * from store")
	store_array = cursor.fetchall()

	# for store in store_array:

	#先写查单个的Store的，后面在通过多线程一起去查多个Store

	store = store_array[0]
	write_store(store)

	store = store_array[1]
	write_store(store)

	book.close()
	cursor.close()
	conn.close()

