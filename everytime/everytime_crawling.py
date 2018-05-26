import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeamScheduler.settings")
import django
django.setup()
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from django.db import models
from everytime.models import EveryTimeData


def crawling_homepage():
    # f = open("class_time.txt",'w')

    queryset = EveryTimeData.objects.all()
    queryset.delete()

    class_data = []

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver',chrome_options=options)
    # driver = webdriver.PhantomJS('/home/pi/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.implicitly_wait(5)

    driver.get('https://everytime.kr/login')

    driver.find_element_by_name('userid').send_keys('hytae1993')
    driver.find_element_by_name('password').send_keys('gusxo1208')
    driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

    driver.get('https://everytime.kr/timetable/wizard/?year=2018&semester=1')
    driver.get_screenshot_as_file('chrome.png')


    def find(driver):
        element = driver.find_elements_by_id("searchLayer")
        if element:
            return element
        else:
            return False


    for i in range(1, 23):  #1,23
        address_1 = '// *[ @ id = "collegeSelect"] / option[' + str(i) + ']'

        driver.find_element_by_xpath(address_1).click()

        for j in range(1, 22):  #22
            address_2 = '// *[ @ id = "majorSelect"] / option[' + str(j) + ']'
            try:
                driver.find_element_by_xpath(address_2).click()
            except NoSuchElementException:
                break
            driver.find_element_by_xpath('//*[@id="searchLayer"]/div[1]/form[2]/p[3]/input').click()
            try:
                length = driver.find_element_by_xpath('//*[@id="searchLayer"]/div[1]/p[2]/em').text
            except StaleElementReferenceException:
                j -= 1
                continue

            for k in range(1, int(length)+1):
                # element = WebDriverWait(driver, 100).until(find)
                address_3 = '// *[ @ id = "searchLayer"] / div[2] / table / tbody / tr[' + str(k) + '] / td[8]'
                try:
                    div_elems = driver.find_element_by_xpath(address_3)
                    element = WebDriverWait(driver, 5).until(find)

                    try:
                        class_data.append(div_elems.text)
                    except StaleElementReferenceException:
                        k = 1
                        continue
                except NoSuchElementException:
                    break
            print('========================NEXT_STEP============================')
            #   time.sleep(5)
    print(len(class_data))
    for i in range(len(class_data)):
        # f.write(class_data[i])
        # f.write("\n")
        EveryTimeData(crawling_data=class_data[i]).save()
    # f.close()

if __name__ == '__main__':
    crawling_homepage()