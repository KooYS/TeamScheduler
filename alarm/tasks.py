from __future__ import absolute_import, unicode_literals
import datetime
from TeamScheduler.celery import app
from schedule.models import User


dt = datetime.datetime.now()   #dt.hour = 현재 시간의 시
alarm_time = 1  #사용자가 팀플 알림받고싶어하는 시간(n시간전)
#team_time_code = 시간 : 요일 : 팀코드 - 카카오아이디 + 카카오아이디 + 카카오아이디 ....
#team_time_code = '10 : 1 : teamcode - kakao_id_1 + kakao_id_2 + kakao_id_3 + kakao_id_4'
team_time_code = '19:6:teamcode -ad'
team_time = int(team_time_code.split(':')[0])
team_day = int(team_time_code.split(':')[1])
team_kakao = team_time_code.split(':')[2]

DB = 'database'

@app.task
def task_number_one():

    #DB SEARCH
    user = User.objects.all()   #DB전체내용불러오기(user 별로 불러오기)
                                #user.kakao_id, user.created_data
    print(user.teamcode)
    print(user.kakao_id)
    print(user.created_date)
    print('========ONE PERIOD==========')