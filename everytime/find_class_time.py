# 요일별 클래스 시간, 건물, 방번호로 정렬
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
django.setup()
from django.shortcuts import render
import numpy as np
from everytime.everytime_crawling import crawling_homepage          # crawling_homepage()
from everytime.everytime_parsing import parsing_data        # parising_data()
from everytime.models import EveryTimeData, ParsedData, AllClass, ClassPerDate


def change_time(time, start_time):
    start_time = str(int(start_time) - 8)
    lec_time = int(start_time)
    for i in range(time):
        start_time += (' ' + str(lec_time + 1))
        lec_time += 1
    # print(start_time)
    return start_time


def return_a(classroom_data, i, j):
    if classroom_data[i][0][j] == '102관':
        return 0
    elif classroom_data[i][0][j] == '103관':
        return 1
    elif classroom_data[i][0][j] == '104관':
        return 2
    elif classroom_data[i][0][j] == '105관':
        return 3
    elif classroom_data[i][0][j] == '106관':
        return 4
    elif classroom_data[i][0][j] == '203관':
        return 5
    elif classroom_data[i][0][j] == '207관':
        return 6
    elif classroom_data[i][0][j] == '208관':
        return 7
    elif classroom_data[i][0][j] == '209관':
        return 8
    elif classroom_data[i][0][j] == '301관':
        return 9
    elif classroom_data[i][0][j] == '302관':
        return 10
    elif classroom_data[i][0][j] == '303관':
        return 11
    elif classroom_data[i][0][j] == '304관':
        return 12
    elif classroom_data[i][0][j] == '305관':
        return 13
    elif classroom_data[i][0][j] == '309관':
        return 14
    elif classroom_data[i][0][j] == '310관':
        return 15
    elif classroom_data[i][0][j] == '공연예술원':
        return 16


# 괄호 character 없애고 요일 list에 추가
def return_date(date, time, building, room):
    time = time.replace("(", "")
    time = time.replace(")", "")
    time = time.replace(",", " ")
    new_time = time[0]
    if ':' in time:
        # print(time)
        new_time += (' ' + time[1:3] + '~')
        if int(time[-2:]) > 0:
            new_time += (str(int(time[-5:-3]) + 1))
        else:
            new_time += time[-5:-3]
    else:
        new_time += (' ' + time[1:])
    # print(new_time)
    if '~' in new_time:
        lecture_time = int(new_time[1:].split('~')[1]) - int(new_time[1:].split('~')[0])
        new_time = new_time[0] + ' ' + change_time(lecture_time - 1, new_time[1:].split('~')[0])
    # print(new_time)
    date.append([new_time, building, room])
    # print(date)


def allschedule(new, old):
    for i in range(len(old)):
        for j in range(len(old[i][0].split(' '))):
            try:
                new.append([int(old[i][0].split(' ')[j]), old[i][1], old[i][2]])
            except ValueError:
                continue

def return_building_name(i):
    if i == 0:
        return '102'
    elif i == 1:
        return '103'
    elif i == 2:
        return '104'
    elif i == 3:
        return '105'
    elif i == 4:
        return '106'
    elif i == 5:
        return '203'
    elif i == 6:
        return '207'
    elif i == 7:
        return '208'
    elif i == 8:
        return '209'
    elif i == 9:
        return '301'
    elif i == 10:
        return '302'
    elif i == 11:
        return '303'
    elif i == 12:
        return '304'
    elif i == 13:
        return '305'
    elif i == 14:
        return '309'
    elif i == 15:
        return '310'
    else:
        return '공원예술원'

def find_room():
    # f = open('parsed_result.txt', 'r')
    queryset1 = AllClass.objects.all()
    queryset1.delete()
    queryset2 = ClassPerDate.objects.all()
    queryset2.delete()

    schedule_parsing_data = []
    for f in ParsedData.objects.all():
        schedule_parsing_data.append(f.schedule_parsing)

    class_data = []  # [시간, 건물, 방번호]
    classroom_data = []
    #while True:
    for index in range(len(schedule_parsing_data)):
        time, room, building = [], [], []
        # line = f.readline()
        # if not line:
        #     break
        for i in range(6):
            try:
                if (schedule_parsing_data[index].split('\t')[2]).split(' ')[i] != '':
                    if (schedule_parsing_data[index].split('\t')[2]).split(' ')[i][-1] == ',':
                        time.append((schedule_parsing_data[index].split('\t')[2]).split(' ')[i][0:-1])
                    else:
                        time.append((schedule_parsing_data[index].split('\t')[2]).split(' ')[i])
            except IndexError:
                pass

            try:
                if (schedule_parsing_data[index].split('\t')[0]).split(' ')[i] != '':
                    building.append((schedule_parsing_data[index].split('\t')[0]).split(' ')[i])
            except IndexError:
                pass

            try:
                if (schedule_parsing_data[index].split('\t')[1]).split(' ')[i] != '':
                    room.append((schedule_parsing_data[index].split('\t')[1]).split(' ')[i])
            except IndexError:
                pass
        class_data.append([time, building, room])
        classroom_data.append([building, room])
    #f.close()
    # f = open('time.txt','w')
    # print(classroom_data)

    # 전체 학기동안 수업있는 강의실들 찾기
    # 1 ~ 17 : 102 103 104 105 106 203 207 208 209 301 302 303 304 305 309 310 공원예술원
    school_building = np.zeros((17, 20, 50))  # 면 = a(건물), 행 = b(층), 열 = c(호)
    for i in range(len(classroom_data)):
        for j in range(len(classroom_data[i][1])):
            try:
                a = return_a(classroom_data, i, j)
            except IndexError:
                try:
                    a = return_a(classroom_data, i, j - 1)
                except IndexError:
                    a = return_a(classroom_data, i, j - 2)

            if classroom_data[i][1][j][0] == 'B':  # 지하 강의실은 데이터에서 포함X
                continue
            else:  # 지상 강의실만 데이터에 포함 : 행 번호가 층 수 그대로
                if len(classroom_data[i][1][j]) == 5:  # 10층 이상
                    b = int(classroom_data[i][1][j][0] + classroom_data[i][1][j][1])
                    c = int(classroom_data[i][1][j][2] + classroom_data[i][1][j][3])
                else:
                    b = int(classroom_data[i][1][j][0])
                    c = int(classroom_data[i][1][j][1] + classroom_data[i][1][j][2])
            school_building[a][b][c] = 1

    for i in range(len(school_building)):
        building_name = return_building_name(i)
        for j in range(len(school_building[i])):
            #print(school_building[i][j])
            AllClass(building_name=building_name, floor=j, exist_class=school_building[i][j]).save()



    # For Test: 102관 강의실들 출력
    # print(school_building[0])
    # print(class_data)
    time_data = []  # [시간,건물,방번호]
    for i in range(len(class_data)):
        for j in range(len(class_data[i][0])):
            try:
                a = class_data[i][0][j]
                b = class_data[i][1][j]
            except IndexError:
                try:
                    b = class_data[i][1][j - 1]
                except IndexError:
                    try:
                        b = class_data[i][1][j - 2]
                    except:
                        continue
            try:
                c = class_data[i][2][j]
            except IndexError:
                try:
                    c = class_data[i][2][j - 1]
                except IndexError:
                    c = class_data[1][2][j - 2]
            time_data.append([a, b, c])
            # f.write(str(time_data[i]) + '\n')
    # f.close()
    # 요일별로 sort
    time_data.sort()
    # print(time_data)
    # 요일별 시간표
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []
    for i in range(len(time_data)):
        if time_data[i][0][0] == '월':
            try:
                return_date(monday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '화':
            try:
                return_date(tuesday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '수':
            try:
                return_date(wednesday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '목':
            try:
                return_date(thursday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '금':
            try:
                return_date(friday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '토':
            try:
                return_date(saturday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue
        elif time_data[i][0][0] == '일':
            try:
                return_date(sunday, time_data[i][0], time_data[i][1], time_data[i][2])
            except IndexError:
                continue

    # print(monday)
    # print(tuesday)
    # print(wednesday)
    # print(thursday)
    # print(friday)
    # print(saturday)
    # print(sunday)

    monday_schedule, tuesday_schedule, wednesday_schedule, thursday_schedule, friday_schedule,\
        saturday_schedule, sunday_schedule  = [], [], [], [], [], [], []

    allschedule(monday_schedule, monday)
    #print(monday_schedule)
    monday_schedule.sort()
    for i in range(len(monday_schedule)):
        ClassPerDate(date_name='월', class_data=monday_schedule[i]).save()
    allschedule(tuesday_schedule, tuesday)
    tuesday_schedule.sort()
    for i in range(len(tuesday_schedule)):
        ClassPerDate(date_name='화', class_data=tuesday_schedule[i]).save()
    allschedule(wednesday_schedule, wednesday)
    wednesday_schedule.sort()
    for i in range(len(wednesday_schedule)):
        ClassPerDate(date_name='수', class_data=wednesday_schedule[i]).save()
    allschedule(thursday_schedule, thursday)
    thursday_schedule.sort()
    for i in range(len(thursday_schedule)):
        ClassPerDate(date_name='목', class_data=thursday_schedule[i]).save()
    allschedule(friday_schedule, friday)
    friday_schedule.sort()
    for i in range(len(friday_schedule)):
        ClassPerDate(date_name='금', class_data=friday_schedule[i]).save()
    allschedule(saturday_schedule, saturday)
    saturday_schedule.sort()
    for i in range(len(saturday_schedule)):
        ClassPerDate(date_name='토', class_data=saturday_schedule[i]).save()
    allschedule(sunday_schedule, sunday)
    sunday_schedule.sort()
    for i in range(len(sunday_schedule)):
        ClassPerDate(date_name='일', class_data=sunday_schedule[i]).save()

    # print(monday_schedule)
    # print(tuesday_schedule)
    # print(wednesday_schedule)
    #print(thursday_schedule)
    # print(friday_schedule)
    # print(saturday_schedule)
    # print(sunday_schedule)


if __name__ == "__main__":
    crawling_homepage()
    parsing_data()
    find_room()