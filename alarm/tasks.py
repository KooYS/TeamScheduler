from __future__ import absolute_import, unicode_literals
import datetime
import logging
from TeamScheduler.celery import app
from schedule.models import *
from schedule.alarm import find
import numpy as np
import time

# task_number_one
# DB SEARCH를 한다. 저장된 시간을 비교해서 시간이 맞다면 나에게 보내기가 이루어진다.
@app.task
def task_number_one():
    #print('TESTSTESTSETSTESTSETSET')

    find(user.alarm_token,info.teamcode)
	return
	
	row = 15
	col = 5
	#DB SEARCH
	infos = TeamInfo.objects.all()
	for info in infos:
		users = User.objects.filter(teamcode=info.teamcode)
		for user in users:
			if user.alarm_token:
				alarm_data = info.alarm_data.split(',')
				alarm_data = list(map(int, alarm_data))
				alarm_data = np.array(alarm_data).reshape(row,col)
				alarm_data = alarm_data.T
				now = datetime.datetime.now()
				#임시 테스츠
				if now.weekday() > 4:
					continue

				index = 0
				#alarm_data[now.weekday()-2] = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
				#for x in alarm_data[now.weekday()-2]:
				for x in alarm_data[now.weekday()]:
					if not x == 0:
						alarm_time = datetime.datetime(now.year, now.month, now.day, 8 + (x * index), 60 - int(info.alarm_data_before_time))
						logger.error(alarm_time)
						logger.error(x)
						delta = now - alarm_time
						delta = delta.seconds // 60
						logger.error(delta)
						if now.hour > 7 and now.hour < 23 and delta > 3:
							find(user.alarm_token,info.teamcode)
					index = index+1