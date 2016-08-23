#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time
import datetime

def get_update_time_period():

	current_day_string = datetime.datetime.now().strftime('%Y-%m-%d')
	current_hour_string = datetime.datetime.now().strftime('%H')

	if current_hour_string[0] == '0':
		current_hour_string = current_hour_string[1]

	current_hour = int(current_hour_string)
	print current_hour
	if  10 <= current_hour < 14:
		print current_day_string + '-1'
	if 14 <= current_hour < 22:
		print current_day_string + '-2'
	if current_hour >= 22 or current_hour < 10:
		print current_day_string + '-3'

if __name__ == '__main__':
	get_update_time_period()