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

if __name__ == '__main__':

	remove_old_file()

	start_date = '2016-08-28'
	end_date = '2016-09-01'

	sql_start_time = datetime.datetime.strptime(start_date,'%Y-%m-%d') + datetime.timedelta(days=-1)
	sql_end_time = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
	sql_start_date = sql_start_time.strftime('%Y-%m-%d')
	sql_end_date = sql_end_time.strftime('%Y-%m-%d')

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

			inventory_table_name = 'inventory' + str(store_id)
			cursor.execute("select DISTINCT wine_id from " + inventory_table_name + " where day_period between %s and %s", (sql_start_date, sql_end_date))
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

