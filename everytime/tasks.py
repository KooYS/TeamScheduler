from __future__ import absolute_import, unicode_literals
import datetime
from TeamScheduler.celery import app
from everytime.find_class_time import find_room
from everytime.everytime_crawling import crawling_homepage
from everytime.everytime_parsing import parsing_data


# task_number_two
@app.task()
def task_number_two():
    print('everytime 크롤링 시작')
    crawling_homepage()
    parsing_data()
    find_room()
    print('everytime 크롤링 끝')
