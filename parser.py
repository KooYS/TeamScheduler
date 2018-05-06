

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 아래 4줄을 추가해 줍니다.
import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
# StudyRoomData import해옵니다
from parsed_data.models import StudyRoomData


class TimeData:
    def __init__(self):
        self.timeData = []


def parse_studyroom():
    mainPath = "body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div > div:nth-child(2) > div > div:nth-child(2) > table > tbody > "

    ##########################################
    # 학술정보원 로그인
    # driver = webdriver.Chrome(
    #    'C:\\Users\\nuke9\Downloads\chromedriver_win32\chromedriver')

    dirver = webdriver.Chrome('Chromedriver_path')  # 경로를 넣어주세요

    driver.implicitly_wait(5)
    driver.get('https://library.cau.ac.kr/#/login')
    driver.find_element_by_name('txtUserID').send_keys('아이디쓰는곳')
    driver.find_element_by_name('txtPwd').send_keys('비밀번호쓰는곳')
    driver.find_element_by_xpath(
        '//*[@ng-submit="portalLogin()"]/div/button').click()

    try:
        element = WebDriverWait(driver, 10).until(
            # By.ID 는 ID로 검색, By.CSS_SELECTOR 는 CSS Selector 로 검색
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
        # tag를 30초 내에 검색, 그렇지 않으면 timeoutexception 발생
        element = WebDriverWait(driver, 30).until(
            # By.ID 는 ID로 검색, By.CSS_SELECTOR 는 CSS Selector 로 검색
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, mainPath + "tr:nth-child(1) > td:nth-child(3) > span"))
        )

    except:
        print("해당 페이지가 30초 안에 열리지 않았습니다.")

    finally:
        html = driver.page_source
    ##########################################

    ##########################################
    TimeTable = []
    for i in range(0, 18):
        TimeTable.append(TimeData())

    soupPath = 'body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div > div > div > div > table > tbody > '
    soup = BeautifulSoup(html, 'html.parser')
    roomInfo = soup.select(soupPath + 'tr > th')
    timeLine = soup.select(soupPath + 'tr > td > div > div > div')

    for i in range(0, 18):
        TimeTable[i].name = roomInfo[2 * i].text
        TimeTable[i].floor = roomInfo[2 * i + 1].text

    data = {}
    i = 0
    for ea in timeLine:
        data[ea.text] = ea.get('class')
        del data[ea.text][0]
        data[ea.text][0] = data[ea.text][0][13:]
        TimeTable[i//(24*6)].timeData.append(data[ea.text][0])
        i = i + 1

    for i in TimeTable:
        for j in range(0, 24):
            i.timeData[j + 1:j + 6] = []
        i.offTime = 0
        for j in range(0, len(i.timeData)):
            if i.timeData[j] == 'off':
                i.offTime |= 1 << j
        driver.quit()

    return TimeTable


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__ == '__main__':
    for i in parse_studyroom():
        StudyRoomData(name=i.name, floor=i.floor, offTime=i.offTime).save()
