import ssl
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib, urllib.request
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium

browser = webdriver.Edge('msedgedriver.exe')

browser.get('http://wallpaperswide.com/vintage-desktop-wallpapers.html')
cats = browser.find_element(By.CSS_SELECTOR, '#left-panel > div.sidebox.categories > div.sidebox-body-r > div > div > div > ul')
links = cats.find_elements(By.TAG_NAME, 'a')
cat_addrs = [link.get_attribute('href') for link in links]

# soup = BeautifulSoup(browser.page_source, 'html.parser')
# cats = soup.select('#left-panel > div.sidebox.categories > div.sidebox-body-r > div > div > div > ul')
# links = cats[0].select('a')
# cat_addrs = ['http://wallpaperswide.com' + link['href'] for link in links]

for cat_addr in cat_addrs:
    browser.get(cat_addr)
    # action = webdriver.ActionChains(browser)

    #모든 페이지를 넘기면서 다운로드
    while True:
        #아이템 리스트
        content = browser.find_element(By.CSS_SELECTOR, '#content')
        wallpapers = content.find_element(By.XPATH, "//ul[@class='wallpapers']")
        huddowns = wallpapers.find_elements(By.ID, 'huddown')
        if len(huddowns) == 0:
            print('error')
        for huddown in huddowns[:2]:
            scr = huddown.get_attribute('onclick')
            browser.execute_script(scr)
            time.sleep(2)
            #프레임 전환 후 다운로드
            notify_frame = browser.find_element(By.ID, 'notifyFrame')
            browser.switch_to.frame(notify_frame)
            browser.execute_script('res_download();')
            #제자리 돌아오기
            time.sleep(1)
            browser.switch_to.default_content()
            browser.execute_script('prevframe_close();')

        try:
            #browser.find_element(By.LINK_TEXT, 'Next »').click()
            next = browser.find_element(By.LINK_TEXT, 'Next »')
            next_link = next.get_attribute('href')
            browser.get(next_link)
            time.sleep(2)
        except:
            break
        
