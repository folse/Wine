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

STORE_LIST = '0102,Fältöversten,STOCKHOLM&0104, ,STOCKHOLM&0106,Garnisonen,STOCKHOLM&0110, ,STOCKHOLM&0113, ,STOCKHOLM&0114,PK-Huset,STOCKHOLM&0116, ,STOCKHOLM&0132,Marieberg,STOCKHOLM&0133, ,STOCKHOLM&0134, ,STOCKHOLM&0135, ,VÄLLINGBY&0137, ,STOCKHOLM&0138, ,STOCKHOLM&0140,Torsplan,STOCKHOLM&0143,Odenplan,STOCKHOLM&0144,Jarlaplan,STOCKHOLM&0145, ,STOCKHOLM&0146, ,STOCKHOLM&0147,Brommaplan,BROMMA&0148, ,HÄSSELBY&0150, ,KISTA&0151,Bromma Blocks,BROMMA&0163,Ringen,STOCKHOLM&0165, ,STOCKHOLM&0166,Söderhallarna,STOCKHOLM&0167, ,STOCKHOLM&0168, ,JOHANNESHOV&0170,Globen,JOHANNESHOV&0171,Liljeholmen,STOCKHOLM&0172, ,STOCKHOLM&0173,Hammarby Sjöstad,STOCKHOLM&0174, ,STOCKHOLM&0176, ,Hägersten&0177, ,BANDHAGEN&0178, ,FARSTA&0180, ,HÄGERSTEN&0182, ,SKÄRHOLMEN&0201, ,SOLNA&0202, ,SUNDBYBERG&0204, ,VAXHOLM&0205, ,HALLSTAVIK&0206, ,NORRTÄLJE&0207, ,SIGTUNA&0208, ,SÖDERTÄLJE&0209, ,SÖDERTÄLJE&0210, ,NYNÄSHAMN&0211, ,LIDINGÖ&0212,Arninge,TÄBY&0213,Mörby Centrum,DANDERYD&0214,Jakobsbergs Centrum,JÄRFÄLLA&0215,Täby Centrum,TÄBY&0216, ,SOLLENTUNA&0217, ,HUDDINGE&0218, ,MÄRSTA&0219,Väsby Centrum,UPPLANDS VÄSBY&0220, ,NACKA&0221, ,TYRESÖ&0222,Haninge Centrum,HANINGE&0223, ,GUSTAVSBERG&0224, ,SALTSJÖBADEN&0225, ,TUMBA&0226,Botkyrka,NORSBORG&0227,Skogås Centrum,SKOGÅS&0228, ,ÅKERSBERGA&0229, ,VALLENTUNA&0230,Orminge Centrum,SALTSJÖ-BOO&0231,Ekerö Centrum,EKERÖ&0232,Kungens Kurva,KUNGENS KURVA&0234,Salem Centrum,RÖNNINGE&0235, ,KUNGSÄNGEN&0236, ,RIMBO&0237,Sickla,NACKA&0238,Mölnvik,GUSTAVSBERG&0239,Västerhaninge centrum,VÄSTERHANINGE&0240,Rotebro,SOLLENTUNA&0241, ,JÄRFÄLLA&0242, ,NYKVARN&0243,Barkarby,JÄRFÄLLA&0244,Mall of Scandinavia,Solna&0245,Haninge Söderby,HANINGE&0246,Häggvik,SOLLENTUNA&0301,Gottsunda centrum,UPPSALA&0302, ,UPPSALA&0303,Stenhagen,UPPSALA&0305,Gränby Centrum,UPPSALA&0306, ,BÅLSTA&0307, ,ENKÖPING&0308, ,TIERP&0309, ,ÖREGRUND&0310, ,SKUTSKÄR&0311,Kvarnen,UPPSALA&0312,Boländerna,UPPSALA&0313, ,KNIVSTA&0401,Nyköping City,NYKÖPING&0402, ,TROSA&0403, ,ESKILSTUNA&0404,Tuna park,ESKILSTUNA&0405, ,TORSHÄLLA&0406, ,KATRINEHOLM&0407, ,STRÄNGNÄS&0408, ,MARIEFRED&0409, ,MALMKÖPING&0410, ,FLEN&0411, ,OXELÖSUND&0412, ,VINGÅKER&0413, ,GNESTA&0414,Gustafsberg,NYKÖPING&0501, ,LINKÖPING&0504,Tornby,LINKÖPING&0505,Gyllentorget,LINKÖPING&0506, ,ÅTVIDABERG&0507, ,MJÖLBY&0509, ,VADSTENA&0510, ,MOTALA&0513, ,NORRKÖPING&0516, ,NORRKÖPING&0517,Ingelsta,NORRKÖPING&0518, ,SÖDERKÖPING&0519, ,VALDEMARSVIK&0520, ,FINSPÅNG&0521, ,KISA&0522, ,ÖDESHÖG&0523, ,ÖSTERBYMO&0524, ,BOXHOLM&0525,Djurgården,Linköping&0601,A6,JÖNKÖPING&0602,Atollen,JÖNKÖPING&0604, ,HABO&0605, ,VÄRNAMO&0606, ,HUSKVARNA&0607, ,NÄSSJÖ&0608, ,VETLANDA&0609, ,EKSJÖ&0610, ,TRANÅS&0611, ,GISLAVED&0612, ,SÄVSJÖ&0613, ,ANEBY&0615, ,GNOSJÖ&0616, ,MULLSJÖ&0618, ,SKILLINGARYD&0619, ,GRÄNNA&0701,Affärshuset Tegner,VÄXJÖ&0702, ,LJUNGBY&0703, ,ÄLMHULT&0704, ,ALVESTA&0705, ,MARKARYD&0706, ,TINGSRYD&0707,Samarkand,VÄXJÖ&0708, ,ÅSEDA&0709, ,LESSEBO&0801,Giraffen,KALMAR&0802, ,KALMAR&0804, ,LÖTTORP&0805, ,BORGHOLM&0806, ,FÄRJESTADEN&0807, ,MÖNSTERÅS&0808, ,OSKARSHAMN&0809, ,VÄSTERVIK&0810, ,VIMMERBY&0811, ,NYBRO&0812, ,HULTSFRED&0813, ,EMMABODA&0814, ,TORSÅS&0815, ,HÖGSBY&0816, ,GAMLEBY&0902, ,VISBY&0903, ,HEMSE&0904, ,SLITE&1001,Wachtmeister,KARLSKRONA&1002,Amiralen,Karlskrona-LYCKEBY&1003, ,RONNEBY&1004, ,KARLSHAMN&1005, ,SÖLVESBORG&1006, ,OLOFSTRÖM&1101, ,KRISTIANSTAD&1103, ,ÅHUS&1104, ,SIMRISHAMN&1105, ,TOMELILLA&1106, ,HÄSSLEHOLM&1107, ,ÄNGELHOLM&1108, ,BÅSTAD&1109, ,KLIPPAN&1110, ,PERSTORP&1111, ,OSBY&1112, ,ÅSTORP&1113, ,ÖRKELLJUNGA&1114, ,BROMÖLLA&1115, ,BROBY&1202, ,MALMÖ&1203,Entré,MALMÖ&1206,Mobilia,MALMÖ&1207, ,MALMÖ&1208,Hansa,MALMÖ&1209,Kronprinsen,MALMÖ&1211,Limhamn,MALMÖ&1213,Västra Hamnen,MALMÖ&1214,Emporia,MALMÖ&1219, ,LOMMA&1220, ,DALBY&1221, ,ARLÖV&1222, ,SKURUP&1224, ,SVEDALA&1225, ,TRELLEBORG&1226, ,VELLINGE&1227,Toppengallerian,HÖLLVIKEN&1230, ,YSTAD&1231, ,SJÖBO&1232, ,STAFFANSTORP&1242,Råå,HELSINGBORG&1243, ,HELSINGBORG&1245,Väla,ÖDÅKRA-VÄLA&1246, ,BJUV&1248, ,LANDSKRONA&1249, ,SVALÖV&1250,Center Syd,LÖDDEKÖPINGE&1252, ,HÖGANÄS&1253,NOVA,LUND&1254, ,LUND&1255,SALUHALLEN,LUND&1256, ,KÄVLINGE&1257, ,ESLÖV&1258, ,HÖÖR&1259, ,HÖRBY&1301, ,HALMSTAD&1302, ,HALMSTAD&1304, ,HYLTEBRUK&1305, ,LAHOLM&1306, ,FALKENBERG&1307, ,VARBERG&1308, ,KUNGSBACKA&1309,Flygstaden,Halmstad&1310,Breared,VARBERG&1311, ,Kungsbacka&1404, ,GÖTEBORG&1406, ,GÖTEBORG&1407,Olskroken,GÖTEBORG&1409, ,GÖTEBORG&1410,Nordstan,GÖTEBORG&1411, ,GÖTEBORG&1412, ,GÖTEBORG&1413,Gårda,GÖTEBORG&1414,Backaplan,GÖTEBORG&1415, ,GÖTEBORG&1416,Bäckebol Homecenter,HISINGS BACKA&1417,Eriksberg,GÖTEBORG&1418,Gamlestaden,GÖTEBORG&1420, ,VÄSTRA FRÖLUNDA&1423, ,ANGERED&1424,Sisjön,ASKIM&1425, ,ÖCKERÖ&1426, ,TORSLANDA&1428, ,MÖLNLYCKE&1429, ,KÅLLERED&1430, ,PARTILLE&1431, ,MÖLNDAL&1432, ,KUNGÄLV&1433, ,SKÄRHAMN&1434, ,STENUNGSUND&1435, ,HENÅN&1436, ,UDDEVALLA&1437, ,UDDEVALLA&1438, ,MUNKEDAL&1439, ,KUNGSHAMN&1440, ,LYSEKIL&1441, ,STRÖMSTAD&1442, ,STRÖMSTAD&1443, ,GREBBESTAD&1501, ,VÄNERSBORG&1503,Anes väg 2,Trollhättan&1504, ,TROLLHÄTTAN&1505, ,ÅMÅL&1506, ,MELLERUD&1507, ,BENGTSFORS&1508,Solkatten,LERUM&1509,Dals-Ed,ED&1511, ,BOLLEBYGD&1512, ,BORÅS&1513,Knalleland,BORÅS&1514, ,LILLA EDET&1515, ,TRANEMO&1516, ,SVENLJUNGA&1517, ,ULRICEHAMN&1518, ,ALINGSÅS&1519, ,KINNA&1520, ,FÄRGELANDA&1521, ,NÖDINGE&1522, ,VÅRGÅRDA&1523, ,HERRLJUNGA&1524,Åhaga,BORÅS&1601, ,MARIESTAD&1602, ,LIDKÖPING&1603, ,GRÄSTORP&1604, ,VARA&1605, ,SKARA&1606, ,SKÖVDE&1607, ,HJO&1608, ,TIDAHOLM&1609, ,FALKÖPING&1610, ,KARLSBORG&1611, ,GÖTENE&1612, ,TÖREBODA&1613, ,GULLSPÅNG&1614, ,TIBRO&1616, ,NOSSEBRO&1617, ,SKÖVDE&1701, ,KARLSTAD&1702,Bergvik,KARLSTAD&1703, ,FORSHAGA&1704, ,KIL&1705, ,SÄFFLE&1706, ,ARVIKA&1707, ,HAGFORS&1708, ,FILIPSTAD&1709, ,KRISTINEHAMN&1710, ,SUNNE&1711, ,MUNKFORS&1712, ,TORSBY&1713, ,ÅRJÄNG&1714, ,GRUMS&1715, ,CHARLOTTENBERG&1716, ,SKOGHALL&1717, ,STORFORS&1801, ,ÖREBRO&1802,Marieberg,ÖREBRO&1803,Eurostop,ÖREBRO&1804,Tybblekullen,Örebro&1805, ,HALLSBERG&1806, ,KUMLA&1807, ,ASKERSUND&1808, ,DEGERFORS&1809, ,KARLSKOGA&1810, ,NORA&1811, ,LINDESBERG&1812, ,HÄLLEFORS&1813, ,LAXÅ&1814, ,KOPPARBERG&1815, ,FJUGESTA&1901,City,VÄSTERÅS&1902,Erikslund,VÄSTERÅS&1903,Hälla,VÄSTERÅS&1905, ,KUNGSÖR&1906, ,ARBOGA&1907, ,KÖPING&1908, ,FAGERSTA&1909, ,SALA&1910, ,HALLSTAHAMMAR&1911, ,SURAHAMMAR&1912, ,NORBERG&1913, ,SKINNSKATTEBERG&1914, ,ÖSTERVÅLA&2001, ,FALUN&2002, ,Borlänge&2003, ,BORLÄNGE&2004,Centrumgallerian,HEDEMORA&2005, ,AVESTA&2006, ,LUDVIKA&2007, ,MORA&2008, ,MALUNG&2009, ,LEKSAND&2010, ,SÄLEN&2011, ,VANSBRO&2012, ,RÄTTVIK&2013, ,ÄLVDALEN&2014, ,SMEDJEBACKEN&2015, ,ORSA&2016,Djurås,Djurås&2017, ,SÄTER&2018, ,IDRE&2101,Gallerian Nian,GÄVLE&2102, ,VALBO&2103, ,GÄVLE&2104, ,SANDVIKEN&2105, ,BOLLNÄS&2106, ,SÖDERHAMN&2107, ,HUDIKSVALL&2108, ,HOFORS&2109, ,LJUSDAL&2110, ,EDSBYN&2111, ,OCKELBO&2112, ,BERGSJÖ&2201, ,HÄRNÖSAND&2202, ,SUNDSVALL&2203,Birsta Sundsvall,SUNDSVALL&2204, ,KVISSLEBY&2205, ,KRAMFORS&2206, ,SOLLEFTEÅ&2207, ,ÖRNSKÖLDSVIK&2208, ,TIMRÅ&2209, ,ÅNGE&2210, ,RAMSELE&2211, ,ÖRNSKÖLDSVIK&2301, ,ÖSTERSUND&2302,Lillänge,ÖSTERSUND&2304, ,BRÄCKE&2305, ,SVEG&2306, ,STRÖMSUND&2307, ,JÄRPEN&2308, ,HAMMARSTRAND&2309, ,SVENSTAVIK&2310, ,ÅRE&2311, ,KROKOM&2312, ,FUNÄSDALEN&2401,Wasagallerian,UMEÅ&2402, ,UMEÅ&2403,Solbacken,SKELLEFTEÅ&2404, ,SKELLEFTEÅ&2405, ,VÄNNÄS&2406, ,LYCKSELE&2407, ,VILHELMINA&2408, ,STORUMAN&2409, ,ÅSELE&2410, ,MALÅ&2411, ,SORSELE&2412, ,DOROTEA&2413, ,NORDMALING&2414, ,NORSJÖ&2415, ,VINDELN&2416,Ersboda,UMEÅ&2417, ,ROBERTSFORS&2418, ,BJURHOLM&2419, ,HEMAVAN&2501, ,LULEÅ&2503,Storheden,LULEÅ&2504, ,PITEÅ&2505, ,BODEN&2506, ,HAPARANDA&2507, ,KIRUNA&2508, ,GÄLLIVARE&2509, ,ARVIDSJAUR&2510, ,KALIX&2511, ,JOKKMOKK&2512, ,ÄLVSBYN&2513, ,PAJALA&2514, ,ÖVERTORNEÅ&2515, ,ARJEPLOG&2516, ,ÖVERKALIX'

def get_store_wine(wine_subcategory,store_id,page):

	request_data = urllib.urlencode({'subcategory':wine_subcategory,'sortdirection':'Ascending','site':store_id,'fullassortment':'0','page':page}) 

	request_url = 'http://www.systembolaget.se/api/productsearch/search?' + request_data.replace('+','%20')

	print request_url

	resp = urllib2.urlopen(request_url).read()  
	resp_json = json.loads(resp)
	meta_data = resp_json['Metadata']
	product_array = resp_json['ProductSearchResults']

	for i in range(len(product_array)):
		
		product = product_array[i]

		product_name = str(product['ProductNameBold']).encode("utf-8") + ' ' + str(product['ProductNameThin']).encode("utf-8")
		product_id = product['ProductId']
		product_inventory = product['QuantityText']
		product_url = product['ProductUrl']

		exist = cursor.execute("SELECT * FROM wine WHERE sys_wine_id = %s", (product_id,))
		result = cursor.fetchone()
		if result == None:
			cursor.execute("INSERT INTO wine(sys_wine_id, name, url) VALUES (%s,%s,%s)", (product_id, product_name, product_url))
    		conn.commit()

		cursor.execute("INSERT INTO store_wine(sys_wine_id, sys_store_id, inventory)VALUES(%s, %s, %s)", (product_id, store_id, product_inventory))
		conn.commit()

	global store_index
	next_page = meta_data['NextPage']
	if next_page > 0:
		get_store_wine(wine_subcategory,store_id,next_page)
	else:
		store_index += 1
		save_store_info(store_array[store_index])

def save_store_info(store_info):
	store_id = store_info.split(',')[0]
	store_name = store_info.split(',')[1]
	store_city = store_info.split(',')[2]

	exist = cursor.execute("select * from store where sys_store_id = %s", (store_id,))
	result = cursor.fetchone()
	if result == None:
		cursor.execute("INSERT INTO store(sys_store_id, name, city) VALUES (%s,%s,%s)", (store_id, store_name, store_city))
    	conn.commit()
	get_store_wine(wine_subcategory,store_id,0)

if __name__ == '__main__':

	conn = psycopg2.connect(database="wine", user="folse", password="", host="localhost", port="5432")
	cursor = conn.cursor()

	wine_subcategory = u'Rött vin'

	store_array = STORE_LIST.split('&')

	store_index = 0
	save_store_info(store_array[store_index])

	cursor.close()
	conn.close()
