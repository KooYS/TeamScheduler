import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
import re
from everytime.models import EveryTimeData, ParsedData



def parsing_data():
    queryset = ParsedData.objects.all()
    queryset.delete()
    ##f = open("class_time.txt", 'r')
    data = []
    #while True:
    #    line = f.readline()
    #    if not line:
    #        break
    #    data.append(line)
    #f.close()
    # f1 = open("aaa.txt",'w')
    # f = open("parsed_result.txt", 'w')
    for f in EveryTimeData.objects.all():
        data.append(f.crawling_data)

    new_class_data = list(set(data))
    new_class_data.sort()
    str_class_data = []
    sort_class_data = []
    for i in range(len(new_class_data)):
        # f1.write(new_class_data[i])
        str_class_data.append(str(new_class_data[i]))

    # 요일+시간, 건물, 방번호 ( 다른 종류 구분 "\t" , 같은 종류끼리 구분: " ")
    building = []
    parsed_data = []
    for i in range(len(str_class_data)):
        parsing = ""
        # 건물 찾기
        building.append(re.findall('[0-9]{3}관{1}|공연예술원', str_class_data[i]))
        # 건물 입력
        try:
            # f.write(" ".join(building[i]) + '\t')
            parsing = " ".join(building[i]) + '\t'
        except IndexError:
            pass

        # 방 번호 입력
        for j in range(5):
            try:
                # f.write(str(re.findall('B?[0-9-]+호{1}', str_class_data[i])[j]))
                parsing += str(re.findall('B?[0-9-]+호{1}', str_class_data[i])[j])
            except IndexError:
                break
            #f.write(" ")
            parsing += " "
        #f.write('\t')
        parsing += '\t'

        # 요일 + 시간 입력
        for j in range(5):
            try:
                # f.write(str(re.findall('[()]?[월화수목금토일]{1}[0-9()]{1}[0-9(),:~]*', str_class_data[i])[j]))
                # f.write(str(re.findall('[월화수목금토일]{1}[0-9()]{1}[0-9(),:~]*', str_class_data[i])[j]))
                parsing += str(re.findall('[월화수목금토일]{1}[0-9()]{1}[0-9(),:~]*', str_class_data[i])[j])
            except IndexError:
                break
            #f.write(" ")
            parsing += " "
        #f.write('\t')
        #parsing += '\t'

        #f.write('\n')
        ParsedData(schedule_parsing=parsing).save()
    #f.close()


if __name__ == '__main__':
    parsing_data()