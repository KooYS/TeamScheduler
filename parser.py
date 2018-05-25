# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
from parsed_data.models import StudyRoomData


class TimeData:
    def __init__(self):
        self.timeData = []


def parse_studyroom():
    mainPath = "body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div > div:nth-child(2) > div > div:nth-child(2) > table > tbody > "

    ##########################################
    # 크롬드라이버 다운로드 링크
    # 'https://sites.google.com/a/chromium.org/chromedriver/downloads'
    #
    # 학술정보원 로그인
    # driver = webdriver.Chrome(
    #    'C:\\Users\\nuke9\Downloads\chromedriver_win32\chromedriver')

    dirver = webdriver.Chrome('Chromedriver_path')
    # 크롬 드라이버 경로를 넣어주세요

    driver.implicitly_wait(3)
    driver.get('https://library.cau.ac.kr/#/login')
    driver.find_element_by_name('txtUserID').send_keys('아이디쓰는곳')
    driver.find_element_by_name('txtPwd').send_keys('비밀번호쓰는곳')
    driver.find_element_by_xpath(
        '//*[@ng-submit="portalLogin()"]/div/button').click()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, mainPath + "tr:nth-child(1) > th:nth-child(1) > span"))
        )
        print(element.text)

    except:
        driver.get('https://library.cau.ac.kr/#/smuf/room/group-study')

    finally:
        driver.get('https://library.cau.ac.kr/#/smuf/room/group-study')
    ##########################################

    ##########################################
    # 팀플룸 예약 페이지 들어가기
    # driver.get('https://library.cau.ac.kr/#/smuf/room/group-study')
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, mainPath + "tr:nth-child(1) > td:nth-child(3) > span"))
        )

    except:
        print("해당 페이지가 30초 안에 열리지 않았습니다.")

    finally:
        html = driver.page_source
    ##########################################
    soupPath = 'body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div > div > div > div > table > tbody > '
    week = datetime.date.today().weekday()
    ##########################################
    weekTable = ['월', '화', '수', '목', '금', '토', '일']
    TimeTable = []
    for j in range(0, 18 * 7):
        TimeTable.append(TimeData())

    for cnt in range(0, 7):
        soup = BeautifulSoup(html, 'html.parser')
        roomInfo = soup.select(soupPath + 'tr > th')
        timeLine = soup.select(soupPath + 'tr > td > div > div > div')

        for i in range(0, 18):
            TimeTable[i + 18 * ((week + cnt) % 7)
                      ].dayWeek = weekTable[(week + cnt) % 7]
            TimeTable[i + 18 * ((week + cnt) % 7)].name = roomInfo[2 * i].text
            TimeTable[i + 18 * ((week + cnt) % 7)
                      ].floor = roomInfo[2 * i + 1].text

        data = {}
        i = 0
        for ea in timeLine:
            data[ea.text] = ea.get('class')
            del data[ea.text][0]
            data[ea.text][0] = data[ea.text][0][13:]
            TimeTable[(i//(24*6)) + 18 * ((week + cnt) % 7)
                      ].timeData.append(data[ea.text][0])
            i = i + 1

        for i in range(0, 18):
            for j in range(0, 24):
                TimeTable[i + 18 * ((week + cnt) % 7)
                          ].timeData[j + 1:j + 6] = []
            TimeTable[i + 18 * ((week + cnt) % 7)].offTime = 0

        for i in range(0, 18):
            for j in range(0, len(TimeTable[i + 18 * ((week + cnt) % 7)].timeData)):
                if TimeTable[i + 18 * ((week + cnt) % 7)].timeData[j] == 'off':
                    if((week + cnt) % 7) == 6:
                        TimeTable[i + 18 * ((week + cnt) %
                                            7) + 13].offTime |= 1 << j
                    else:
                        TimeTable[i + 18 * ((week + cnt) %
                                            7)].offTime |= 1 << j
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/form/div[2]/span').click()

        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "body > div.k-animation-container > div > div:nth-child(2) > ul > li:nth-child(2)"))
            )

        except:
            print("해당 페이지가 5초 안에 열리지 않았습니다.")

        finally:
            time.sleep(1)
            driver.find_element_by_xpath(
                "//*[@data-offset-index='%s']" % (cnt + 1)).click()
            time.sleep(1)
            html = driver.page_source
    driver.quit()
    return TimeTable


if __name__ == '__main__':
    for i in parse_studyroom():
        StudyRoomData(name=i.dayWeek + " " + i.name,
                      floor=i.floor, offTime=i.offTime).save()
