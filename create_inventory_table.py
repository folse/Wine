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

sys.setdefaultencoding('utf8')   
sys.setrecursionlimit(1000000)

def create_table(store):
	store_id = str(store[0])
	sql = "CREATE TABLE inventory"+ store_id +" (ID serial PRIMARY KEY,wine_id int4,inventory int4,created_at timestamp(6) NULL,updated_at timestamp(6) NULL,wine_name varchar(256),wine_number varchar(64),day_period varchar(64));"
	cursor.execute(sql)
	conn.commit()

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("select * from store")
	store_array = cursor.fetchall()

	for store in store_array:
		create_table(store)

	cursor.close()
	conn.close()
