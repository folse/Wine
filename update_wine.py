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

def update_wine_info(index_id):
	cursor.execute("SELECT * FROM wine WHERE id = %s", (index_id,))
	row = cursor.fetchone()
	if row != None:	
		wine_number = row[11]
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

	try:
		resp = urllib2.urlopen(req).read()
		parse_wine_info(resp,wine_number)
	except Exception, e:
		print e
		time.sleep(300)
		resp = urllib2.urlopen(req).read()
		parse_wine_info(resp,wine_number)

def parse_wine_info(resp,wine_number):

	data = json.loads(resp)

	if data.has_key('Artikeldetaljer'):

		wine_detail = data['Artikeldetaljer']

		wine_info = ''
    	sales_start = ''
    	alcohol = ''
    	color = ''
    	fragrance = ''
    	ingredient = ''
    	sugar = ''
    	producer = ''
    	supplier = ''

    	if data.has_key('Artiklar'):
			for i in range(len(data['Artiklar'])):
				wine_detail_number = data['Artiklar'][i]['ArtikelNr']
				if wine_detail_number == wine_number:
					wine_info = data['Artiklar'][i]

			if wine_info.has_key('Saljstartsdatum'):
				sales_start = get_date_from_timestamp(wine_info['Saljstartsdatum'])

			if wine_info.has_key('Alkoholhalt'):
				alcohol = str(wine_info['Alkoholhalt']) + ' %'

			if wine_detail.has_key('Farg'):
				color = wine_detail['Farg']

			if wine_detail.has_key('Doft'):
				fragrance = wine_detail['Doft']

			if wine_detail.has_key('Ravara'):
				ingredient = wine_detail['Ravara']

			if wine_detail.has_key('Sockerhalt'):
				sugar = wine_detail['Sockerhalt'] + ' g/l'

			if wine_info.has_key('Producent'):
				producer = wine_info['Producent']

			if wine_info.has_key('Leverantor'):
				supplier = wine_info['Leverantor']

			print wine_number
			print sales_start
			cursor.execute("UPDATE wine SET(sales_start, alcohol, color, fragrance, ingredient, sugar, producer, supplier, updated_at) = (%s,%s,%s,%s,%s,%s,%s,%s,%s) WHERE number = %s", (sales_start, alcohol, color, fragrance, ingredient, sugar, producer, supplier, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wine_number))
			conn.commit()

def get_date_from_timestamp(time_stamp_info):
	
	time_stamp = 0

	if time_stamp_info[6] == '1':
		time_stamp = int(time_stamp_info[6:16])
	else:
		time_stamp = int(time_stamp_info[6:15])

	return time.strftime("%Y-%m-%d", time.gmtime(time_stamp + 7200))

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="postgres", password="makeFuture", host="localhost", port="5432")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM wine")
	result = cursor.fetchall()
	# rows_count = result[0]

	for row in result:
		# print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>   " + str(i+1)
		#update_wine_info(i+1)

		#just for once fix

		wine_name = row[1]

		if wine_name[-5:] == ' None':
			print wine_name
			wine_name = wine_name[:len(wine_name)-5]
			print wine_name

			cursor.execute("UPDATE wine SET(name) = (%s) WHERE number = %s", (wine_name, wine_number))
			conn.commit()

		

	cursor.close()
	conn.close()
