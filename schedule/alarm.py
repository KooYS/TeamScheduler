from celery import Celery
from celery.schedules import crontab
import datetime

dt = datetime.datetime.now()   #dt.hour = 현재 시간의 시
alarm_time = 1  #사용자가 팀플 알림받고싶어하는 시간(n시간전)
#team_time_code = 시간 : 요일 : 팀코드 - 카카오아이디 + 카카오아이디 + 카카오아이디 ....
#team_time_code = '10 : 1 : teamcode - kakao_id_1 + kakao_id_2 + kakao_id_3 + kakao_id_4'
team_time_code = '19:6:teamcode -ad'
team_time = int(team_time_code.split(':')[0])
team_day = int(team_time_code.split(':')[1])
team_kakao = team_time_code.split(':')[2]


app = Celery('tasks',broker='amqp://aaa:bbb@localhost:5672//')
app.conf.timezone = 'Asia/Seoul'

def setup_period_tasks(sender, **kwargs):
    if dt.hour == team_time - alarm_time:
        sender.add_period_task(
            crontab(hour=team_time, minute=6, day_of_week=team_day),
            test.s(team_kakao)
        )

@app.task
def test(arg):
    print(arg)






