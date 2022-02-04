from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import schedule
import random
import telepot
import datetime

browser = webdriver.Chrome('C:/chromedriver.exe')
browser.set_window_position(3000,0) 

def connectNaver():
    browser.get('https://www.naver.com')

    browser.implicitly_wait(10)

    browser.find_element(By.CSS_SELECTOR, 'a.nav.shop').click()
    time.sleep(2)


def search(str):
    bot.sendMessage(mc, str)
    connectNaver()

    search = browser.find_element(By.CSS_SELECTOR, 'input.co_srh_input._input')
    search.click()

    search.send_keys(str)
    search.send_keys(Keys.ENTER)

    scrollY()

    items = browser.find_elements(By.CSS_SELECTOR, '.basicList_item__2XT81')

    links = []

    for item in items:
        name = item.find_element(By.CSS_SELECTOR, '.basicList_title__3P9Q7').text
        try:
            mall = item.find_element(By.CSS_SELECTOR, '.basicList_mall__sbVax').text            
        except:
            print('mall except')

        if mall not in mall_list:
            continue

        #print(mall)
        try:
            adv = item.find_element(By.CSS_SELECTOR, '.ad_ad_stk__12U34').text
        except:
            adv = 'NONE'

        link = item.find_element(By.CSS_SELECTOR, '.basicList_title__3P9Q7 > a').get_attribute('href')
        if '광고' in adv:
            links.append(link)
            bot.sendMessage(mc, mall + '\n' + name)
#            bot.sendMessage(mc, link)

    openUrl(links)

def openUrl(links):
    for url in links:
        browser.get(url)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randrange(1, 17))
        browser.get('https://www.naver.com')
        time.sleep(1)
    
def scrollY():
    before_h = browser.execute_script('return window.scrollY')

    while True:
        browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
        time.sleep(1)
        after_h = browser.execute_script('return window.scrollY')
        if after_h == before_h:
            break;
        before_h = after_h

def loop_fucntion():
    #time.sleep(random.randrange(1, 1000))
    #bot.sendMessage(mc, datetime.datetime.now())
    search('네이처하이크자충매트')
    search('네이처자충매트')
    search('네이처하이크매트')
    search('네이처하이크 자충매트')
    #search('블랙코팅타프')
    #browser.quit() 

mall_list = ['프로덕트온라인', 'ONEHEART', 'KALALA', '어썸1647', '당돌브라더스', 'BESTBAIT', '주말N캠핑', '플레이던스']

token = '5008461782:AAEqAxUVEIKOYhZAr4gvj1UIqNkN1tCvD7k'
mc = '1950703241'
bot = telepot.Bot(token)

schedule.every(20).minutes.do(loop_fucntion)

loop_fucntion()

while False:
    schedule.run_pending()
    time.sleep(1)

#search('네이처하이크자충매트')
#search('블랙코팅타프')
#search('네이처하이크매트')
#search('네이처하이크에어매트')
#search('아이언행어')
#browser.quit()



#browser.get('https://www.naver.com')
    #print(price)
    #print(link)
