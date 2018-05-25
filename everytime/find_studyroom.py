
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
from everytime.models import StudyRoomData
import datetime

def studyroom():
    time = {0: 'A.M 0시 ~ A.M 1시', 1: 'A.M 1시 ~ A.M 2시', 2: 'A.M 2시 ~ A.M 3시', 3: 'A.M 3시 ~ A.M 4시',
            4: 'A.M 4시 ~ A.M 5시', 5: 'A.M 5시 ~ A.M 6시', 6: 'A.M 6시 ~ A.M 7시', 7: 'A.M 7시 ~ A.M 8시',
            8: 'A.M 8시 ~ A.M 9시', 9: 'A.M 9시 ~ A.M 10시', 10: 'A.M 10시 ~ A.M 11시', 11: 'A.M 11시 ~ P.M 12시',
            12: 'P.M 12시 ~ P.M 1시', 13: 'P.M 1시 ~ P.M 2시', 14: 'P.M 2시 ~ P.M 3시', 15: 'P.M 3시 ~ P.M 4시',
            16: 'P.M 4시 ~ P.M 5시', 17: 'P.M 5시 ~ P.M 6시', 18: 'P.M 6시 ~ P.M 7시', 19: 'P.M 7시 ~ P.M 8시',
            20: 'P.M 8시 ~ P.M 9시', 21: 'P.M 9시 ~ P.M 10시', 22: 'P.M 10시 ~ P.M11시', 23 : 'P.M 11시 ~ P.M 12시'}

    dt = datetime.datetime.now()
    query = StudyRoomData.objects.all()
    notice = '예약가능한 스터디룸:' + '\n'
    for data in query:
        reserve_time = ''
        notice = notice + '<' + data.name + '\t' + data.floor
        reserve_time = str(bin(data.offTime))[:1:-1]
        # print(reserve_time)
        for i in range(len(reserve_time)):
            if reserve_time[i] == '1':
                if (dt.hour+2) < i:
                    notice = notice + '\t' + time.get(i)
        notice = notice + '>' + '\n'

    print(notice)

    return notice


if __name__ == '__main__':
    studyroom()
