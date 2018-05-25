# 메인 함수
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
import datetime
import numpy as np
from everytime.models import EveryTimeData, ParsedData, AllClass, ClassPerDate


def empty():
    notice = ''
    school_building = np.zeros((17, 20, 50), dtype=int)
    classdata = []
    # 1 ~ 17 : 102 103 104 105 106 203 207 208 209 301 302 303 304 305 309 310 공원예술원
    building = {0: '102', 1: '103', 2: '104', 3: '105', 4: '106', 5: '203', 6: '207', 7: '208', 8: '209',
                9: '301', 10: '302', 11: '303', 12: '304', 13: '305', 14: '309', 15: '310', 16: '공연예술원'}
    building_2 = {'102관': 0, '103관': 1, '104관': 2, '105관': 3, '106관': 4, '203관': 5, '207관': 6, '208관': 7,
                  '209관': 8, '301관': 9, '302관': 10, '303관': 11, '304관': 12, '305관': 13, '309관': 14,
                  '310관': 15, '공연예술원': 16}
    date = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    time = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12, 21: 13, 22: 14}
    dt = datetime.datetime.now()

    for i in range(17):
        # filter_name = building.get(i) + '\t' + str(j) + "층"
        filter_name = building.get(i)
        queryset = AllClass.objects.filter(building_name=filter_name)
        for data in queryset:
            j = int(data.floor)
            for k in range(50):
                if k == 0:
                    school_building[i][j][k] = int(data.exist_class.split('.')[0].split('[')[1])
                else:
                    school_building[i][j][k] = int(data.exist_class.split('.')[k])
                    # print(school_building[i][j][k])

    # queryset = AllClass.objects.filter(building_name=310)
    # for data in queryset:
    #     print(data.exist_class)
    #     print(int(data.exist_class.split('.')[0].split('[')[1]))
    #     print(int(data.exist_class.split('.')[1]))

    queryset = ClassPerDate.objects.filter(date_name=date.get(dt.weekday()))
    # print(date.get(dt.weekday()))
    for data in queryset:
        classdata.append(data.class_data)

    # print(classdata)
    # print(len(classdata))
    # print(classdata[0])
    # print(classdata[0].split('[')[1].split(',')[0])
    # print(classdata[0].split(' ')[1].split('\'')[1])
    # print(classdata[0].split(' ')[2].split('\'')[1].split('호')[0])
    # print(building_2.get(classdata[0].split(' ')[1].split('\'')[1]))      # 면
    # print(classdata[0].split(' ')[2].split('\'')[1].split('호')[0][0])    # 행
    # print(classdata[0].split(' ')[2].split('\'')[1].split('호')[0][1:])   # 열

    # dt.hour에 수업있는 강의실 = 2
    for i in range(len(classdata)):
        if time.get(dt.hour+1) == int(classdata[i].split('[')[1].split(',')[0]):
        # if time.get(11) == int(classdata[i].split('[')[1].split(',')[0]):  # 시간 당 test용도
            #print(classdata[i])
            j = building_2.get(classdata[i].split(' ')[1].split('\'')[1])  # 면
            k = classdata[i].split(' ')[2].split('\'')[1].split('호')[0][0] # 행
            if k == 'B':  # 지하는 생각X
                continue
            else:
                l = classdata[i].split(' ')[2].split('\'')[1].split('호')[0][1:] # 열
                if '-' in l:
                    # print(l)
                    l = l.split('-')[0]
            # print(j,k,l)
            # print(int(j),int(k),int(l))
            school_building[int(j)][int(k)][int(l)] = 2

    # for i in range(17):
    #     for j in range(20):
    #         print(school_building[i][j])

    for i in range(17):
        building_name = building.get(i)
        if i != 16:
            notice_str = '<' + building_name + '관: '
        else:
            notice_str = '<' + building_name + ': '
        for j in range(20):
            for k in range(50):
                if school_building[i][j][k] == 1:
                    if k < 10:
                        notice_str = notice_str + '\t' + str(j) + '0' + str(k) + '호'
                    else:
                        notice_str = notice_str + '\t' + str(j) + str(k) + '호'

        notice_str += '>'
        notice = notice + notice_str + '\n'

    print(notice)
    return notice

if __name__ == "__main__":
    empty()
