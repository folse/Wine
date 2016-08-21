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

if __name__ == '__main__':

	remove_old_file()

	book = xlsxwriter.Workbook(inventory_file_name)
	sheet = book.add_worksheet()

	row = -3
	col = 0

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select * from store")
	store_array = cursor.fetchall()
	for store in store_array:

		if store != None:

			store_id = str(store[0])
			store_name = str(store[1])

			print store_id

			row +=3

			store_info = 'Store Id: ' + store_id + ', Store Name: ' + store_name
			
			sheet.write(row,col,store_info)
			sheet.write(row+1,col,'Product Name')
			sheet.write(row+1,col+1,'Product Id')
			sheet.write(row+1,col+2,get_day(1)[5:] + ' ' + '22:00')

			cursor.execute("select * from inventory where store_id = %s and day_period = %s", (store_id, get_last_day_period()))
			inventory_array = cursor.fetchall()

			for inventory in inventory_array:

				wine_id = inventory[1]
				wine_name = inventory[6]
				wine_number = inventory[7]
				wine_inventory = inventory[3]

				sheet.write(row+2,col,wine_name)
				sheet.write(row+2,col+1,wine_number)
				sheet.write(row+2,col+2,wine_inventory)

				row +=1

	book.close()
	cursor.close()
	conn.close()
	


