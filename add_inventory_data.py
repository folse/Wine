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

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()

	cursor.execute("select wine_id from inventory")
	wine_id_array = cursor.fetchall()
	for i in range(len(wine_id_array)):

		wine_id = wine_id_array[i]
		print i
		cursor.execute("select * from wine where id = %s", wine_id)
		wine = cursor.fetchone()
		wine_name = wine[1]
		wine_number = wine[11]
		cursor.execute("UPDATE inventory SET(wine_name, wine_number) = (%s, %s) WHERE wine_id = %s", (wine_name, wine_number, wine_id))
		conn.commit()
	
	cursor.close()
	conn.close()

	# ---------- 

	# conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	# cursor = conn.cursor()

	# cursor.execute("UPDATE inventory SET day_period = '2016-08-21-3'")
	# conn.commit()
	
	# cursor.close()
	# conn.close()
