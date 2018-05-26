from __future__ import absolute_import, unicode_literals
from everytime.studyroom import parse_studyroom
from TeamScheduler.celery import app

# task_number_three
@app.task()
def task_number_three():
    print('studyroom 크롤링 시작')
    parse_studyroom()
    print('studyroom 크롤링 끝')