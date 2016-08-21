#!/usr/bin/python 
#coding=utf-8

import os
import psycopg2
import urllib2
import json
import time
import datetime
import sys 
reload(sys)
sys.setdefaultencoding('utf8')   

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM wine")
	result = cursor.fetchall()

	for row in result:
		wine_name = row[1]

		if wine_name[-5:] == ' None':
			print wine_name
			wine_name = wine_name[:len(wine_name)-5]
			print wine_name

			cursor.execute("UPDATE wine SET(name) = (%s) WHERE id = %s", (wine_name, row[0]))
			conn.commit()

	cursor.close()
	conn.close()
