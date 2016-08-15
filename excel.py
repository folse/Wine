import os
import json
import time
import urllib
import urllib2
from xlwt import Workbook
import xlrd

import sys  
reload(sys)

inventory_file_name = 'inventory_%s.xls' % time.strftime('%Y-%m-%d',time.localtime(time.time()))


def get_store_wine(wine_subcategory,store_id,page):

	read_book = xlrd.open_workbook(inventory_file_name)
	read_sheet = read_book.sheet_by_index(0)
	sheet.write(read_sheet.nrows,0,product_name)
	sheet.write(read_sheet.nrows,1,product_id)
	sheet.write(read_sheet.nrows,2,product_inventory)
	book.save(inventory_file_name)

def remove_old_file():
	if os.path.isfile(inventory_file_name): 
		os.remove(inventory_file_name)

if __name__ == '__main__':

	remove_old_file()

	wine_subcategory = u'Rött vin'

	book = Workbook(encoding = 'utf-8')
	sheet = book.add_sheet(wine_subcategory)

	book.save(inventory_file_name)


	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select max(id) from wine")
	result = cursor.fetchone()
	for i in xrange(1,result[0]+1):
		exist = cursor.execute("select * from wine where id = %s", [i])
		result = cursor.fetchone()
		if result != None:

			read_book = xlrd.open_workbook(inventory_file_name)
			read_sheet = read_book.sheet_by_index(0)

			sheet.write(read_sheet.nrows,0,store_info)
			sheet.write(read_sheet.nrows+1,0,'Product Name')
			sheet.write(read_sheet.nrows+1,1,'Product Id')
			sheet.write(read_sheet.nrows+1,2,time.strftime('%H:%M:%S',time.localtime(time.time())))
			book.save(inventory_file_name)
	
	cursor.close()
	conn.close()








			# store_info = store_array[i]
		# store_id = store_info.split(',')[0]

		# read_book = xlrd.open_workbook(inventory_file_name)
		# read_sheet = read_book.sheet_by_index(0)
		# sheet.write(read_sheet.nrows,0,store_info)
		# sheet.write(read_sheet.nrows+1,0,'Product Name')
		# sheet.write(read_sheet.nrows+1,1,'Product Id')
		# sheet.write(read_sheet.nrows+1,2,time.strftime('%H:%M:%S',time.localtime(time.time())))
		# book.save(inventory_file_name)
