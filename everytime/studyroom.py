import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# from everytime.models import StudyRoomData
from PIL import Image


class TimeData:
    def __init__(self):
        self.timeData = []


def image_crop(image):
    img = Image.open(image)
    # area = (600, 306, 1490, 870)
    area = (595, 275, 1560, 870)
    cropped_img = img.crop(area)
    cropped_img.save(settings.MEDIA_ROOT+'studyroom_time.png')


def parse_studyroom():

    # queryset = StudyRoomData.objects.all()
    # queryset.delete()

    mainPath = "body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div > div:nth-child(2) > div > div:nth-child(2) > table > tbody > "

    ##########################################
    # 학술정보원 로그인

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver',chrome_options=options)

    driver.implicitly_wait(5)
    driver.get('https://library.cau.ac.kr/#/login')
    driver.find_element_by_name('txtUserID').send_keys('dream1208')
    driver.find_element_by_name('txtPwd').send_keys('gusxo1208!')
    driver.find_element_by_xpath('//*[@ng-submit="portalLogin()"]/div/button').click()

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

    driver.get_screenshot_as_file('chrome.png')

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

    driver.get_screenshot_as_file('studyroom.png')
    image_crop('studyroom.png')

#   for i in range(0, 18):
#       TimeTable[i].name = roomInfo[2 * i].text
#       TimeTable[i].floor = roomInfo[2 * i + 1].text

#   data = {}
#   i = 0
#   for ea in timeLine:
#       data[ea.text] = ea.get('class')
#       del data[ea.text][0]
#       data[ea.text][0] = data[ea.text][0][13:]
#       TimeTable[i//(24*6)].timeData.append(data[ea.text][0])
#       i = i + 1

#   for i in TimeTable:
#       for j in range(0, 24):
#           i.timeData[j + 1:j + 6] = []
#       i.offTime = 0
#       for j in range(0, len(i.timeData)):
#           if i.timeData[j] == 'off':
#               i.offTime |= 1 << j
#       driver.quit()

#    for i in TimeTable:
#        StudyRoomData(name=i.name, floor=i.floor, offTime=i.offTime).save()

