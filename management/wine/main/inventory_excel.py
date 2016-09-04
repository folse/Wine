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

inventory_file_name = 'inventory.xlsx'

def remove_old_file():
	if os.path.isfile(inventory_file_name): 
		os.remove(inventory_file_name)

def get_day(start_time, fix_day):

	if start_time == None:
		start_time = datetime.datetime.now()

	last_time = start_time + datetime.timedelta(days=-fix_day)
	day_string = last_time.strftime('%Y-%m-%d')

	return day_string

def write_days_title(self, row, days_count):

	hour_period_array = ['10:00', '14:00', '22:00']
	for i in xrange(0,days_count+1):
		j = 3
		while (j > 0):
			j-=1
			day_period = get_day(self.end_day,i)[5:] + ' ' + hour_period_array[j]
			column = i*3+(3-j)+1
			self.sheet.write(row,column,day_period)

def write_period_inventory(self, wine_array, store_id, day_period, col):

	inventory_dict = {}

	inventory_table_name = 'inventory' + str(store_id)
	sql = "select * from " + inventory_table_name + " where day_period = '%s'" % day_period

	self.cursor.execute(sql)
	inventory_array = self.cursor.fetchall()

	for inventory in inventory_array:

		wine_id = inventory[1]
		wine_inventory = inventory[2]
		inventory_dict[wine_id] = wine_inventory

	for wine in wine_array:

		wine_id = wine[0]

		if inventory_dict.has_key(wine_id):
			self.sheet.write(self.inventory_row, col, inventory_dict[wine_id])
		else:
			self.sheet.write(self.inventory_row, col, 0)

		self.inventory_row +=1

def write_store_period_wines(self, store_id):

	sql_start_time = self.start_day + datetime.timedelta(days=-1)
	sql_end_time = self.end_day + datetime.timedelta(days=1)
	sql_start_date = sql_start_time.strftime('%Y-%m-%d')
	sql_end_date = sql_end_time.strftime('%Y-%m-%d')

	inventory_table_name = 'inventory' + str(store_id)
	self.cursor.execute("select DISTINCT wine_id, wine_name, wine_number from " + inventory_table_name + " where day_period between %s and %s", (sql_start_date, sql_end_date))
	wine_array = self.cursor.fetchall()
	for wine in wine_array:

		wine_id = str(wine[0])
		wine_name = str(wine[1])
		wine_number = str(wine[2])

		self.row +=1

		self.sheet.write(self.row, 0, wine_name)
		self.sheet.write(self.row, 1, wine_number)

	return wine_array

def write_store(self, store):

	store_id = str(store[0])
	store_name = str(store[1])

	self.row +=3

	store_info = 'Store Id: ' + store_id + ', Store Name: ' + store_name
	
	self.sheet.write(self.row, self.col, store_info)
	self.sheet.write(self.row+1, self.col, 'Product Name')
	self.sheet.write(self.row+1, self.col+1, 'Product Id')
	write_days_title(self, self.row+1, self.days_count)

	self.row = self.row+1

	wine_array = write_store_period_wines(self, store_id)

	period_array = ['1', '2', '3']
	for i in xrange(0, self.days_count + 1):
		j = 3
		while (j > 0):
			j-=1
			day_period = get_day(self.end_day,i) + '-' + period_array[j]
			column = i*3+(3-j)+1
			write_period_inventory(self, wine_array, store_id, day_period, column)
			self.inventory_row -= len(wine_array)

	self.inventory_row = self.inventory_row + len(wine_array) + 4

	print store_id

class WineExcel:

	def __init__(self, start_date, end_date):

		remove_old_file()

		self.book = xlsxwriter.Workbook(inventory_file_name)
		self.sheet = self.book.add_worksheet()
		
		self.row = -3
		self.col = 0
		self.inventory_row = 2

		self.start_day = datetime.datetime.strptime(start_date,'%Y-%m-%d')
		self.end_day = datetime.datetime.strptime(end_date,'%Y-%m-%d')
		self.days_count = (self.end_day-self.start_day).days

	def export_inventory(self):

		conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
		self.cursor = conn.cursor()
		self.cursor.execute("select * from store")
		store_array = self.cursor.fetchall()

		for store in store_array:
			write_store(self, store)

		#先写查单个的Store的，后面在通过多线程一起去查多个Store

		# store = store_array[0]
		# write_store(self, store)

		self.book.close()
		self.cursor.close()
		conn.close()

		return True

if __name__ == '__main__':

	wineExcel = WineExcel('2016-08-28','2016-09-01')
	wineExcel.export_inventory()

