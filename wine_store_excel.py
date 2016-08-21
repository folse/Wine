#!/usr/bin/python 
#coding=utf-8
import os
import json
import time
import datetime
import xlsxwriter
import psycopg2

import sys  
reload(sys)
sys.setdefaultencoding('utf8')

wine_file_name = 'wine_%s.xlsx' % time.strftime('%Y-%m-%d',time.localtime(time.time()))

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

	update_time_period = get_last_day_period()

	book = xlsxwriter.Workbook(wine_file_name)
	sheet = book.add_worksheet()

	row = -3

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select * from store")
	store_array = cursor.fetchall()
	for store in store_array:

		if store != None:

			store_id = str(store[0])
			store_name = str(store[1])

			store_info = 'Store Id: ' + store_id + ', Store Name: ' + store_name

			print store_id

			row += 3

			sheet.write(row,0,store_info)
			sheet.write(row+1,0,'Product Name')
			sheet.write(row+1,1,'Product Id')
			sheet.write(row+1,2,'Säljstart')
			sheet.write(row+1,3,'Alkoholhalt')
			sheet.write(row+1,4,'Färg')
			sheet.write(row+1,5,'Doft')
			sheet.write(row+1,6,'Råvaror')
			sheet.write(row+1,7,'Sockerhalt')
			sheet.write(row+1,8,'Producent')
			sheet.write(row+1,9,'Leverantör')

			cursor.execute("select wine_id from inventory where store_id = %s and day_period = %s", (store_id, update_time_period))
			wine_id_array = cursor.fetchall()
			for wine_id in wine_id_array:

				cursor.execute("select * from wine where id = %s", wine_id)
				wine = cursor.fetchone()

				sheet.write(row+2,0,wine[1])
				sheet.write(row+2,1,wine[11])
				sheet.write(row+2,2,wine[2])
				sheet.write(row+2,3,wine[3])
				sheet.write(row+2,4,wine[4])
				sheet.write(row+2,5,wine[5])
				sheet.write(row+2,6,wine[6])
				sheet.write(row+2,7,wine[7])
				sheet.write(row+2,8,wine[8])
				sheet.write(row+2,9,wine[9])

				row += 1

	book.close()
	cursor.close()
	conn.close()

