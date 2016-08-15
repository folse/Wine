#!/usr/bin/python 
#coding=utf-8
import os
import psycopg2
import urllib2
import json
import sys  
reload(sys)
sys.setdefaultencoding('utf8')   

def update_wine_info(index_id):
	cursor.execute("SELECT * FROM wine WHERE id = %s", (index_id,))
	row = cursor.fetchone()
	if row != None:	
		wine_number = row[12]
		get_wine_info(wine_number)

def get_wine_info(wine_number):
	url = 'https://api.systembolaget.se/V4/artikel/' + wine_number
	username = 'DMZ1\SybApi'
	password = 'zc3R21Q8nJ4y8Pj1A6uB'
	send_headers = {
	 'Host':'api.systembolaget.se',
	 'User-Agent':'Systembolaget/2.1 (iPhone; iOS 10.0; Scale/2.00)',
	 'Authorization':'Basic RE1aMVxTeWJBcGk6emMzUjIxUThuSjR5OFBqMUE2dUI=',
	 'Connection':'keep-alive'
	}
	  
	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None, url, username, password)
	urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

	req = urllib2.Request(url,headers=send_headers)
	data = urllib2.urlopen(req).read()

	wine = json.loads(data)

	print wine.keys()
	print wine["Artikeldetaljer"]["Ravara"]

if __name__ == '__main__':

	os.chdir("scrapy_wine")

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM wine")
	rows_count = cursor.fetchone()[0]

	for i in range(rows_count):
		update_wine_info(i+1)
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(i)

	cursor.close()
	conn.close()
