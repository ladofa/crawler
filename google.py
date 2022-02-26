# https://ecsimsw.tistory.com/entry/Crawling-Scraping?category=869268
# http://pythonstudy.xyz/python/article/404-%ED%8C%8C%EC%9D%B4%EC%8D%AC-Selenium-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import ssl
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib, urllib.request
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

###initial set

folder = ".image/"
url = "https://www.google.com/search"
searchItem = "door"
size = 3000

params ={
   "q":searchItem
   ,"tbm":"isch"
   ,"sa":"1"
   ,"source":"lnms&tbm=isch"
}

url = url+"?"+urllib.parse.urlencode(params)
browser = webdriver.Edge('msedgedriver.exe')
time.sleep(0.5)
browser.get(url)
html = browser.page_source
time.sleep(0.5)

### get number of image for a page

soup_temp = BeautifulSoup(html,'html.parser')
img4page = len(soup_temp.findAll("img"))

### page down 

elem = browser.find_element_by_tag_name("body")
imgCnt = 0
while imgCnt < size:
    elem.send_keys(Keys.PAGE_DOWN)
    print(imgCnt)
    time.sleep(0.2)
    imgCnt += img4page


photo_grid_boxes = browser.find_elements(By.XPATH, '//div[@class="bRMDJf islir"]')

print('Scraping links')

links = []

for box in photo_grid_boxes:
    try:
        imgs = box.find_elements(By.TAG_NAME, 'img')

        for img in imgs:
            # self.highlight(img)
            src = img.get_attribute("src")

            # Google seems to preload 20 images as base64
            if str(src).startswith('data:'):
                src = img.get_attribute("data-iurl")
            links.append(src)

    except Exception as e:
        print('[Exception occurred while collecting links from google] {}'.format(e))

links = list(dict.fromkeys(links))

print('Collect links done. Site: {}, Keyword: {}, Total: {}'.format('google', searchItem, len(links)))
browser.close()


saveDir = os.path.join(folder, searchItem)

# for https
ssl._create_unverified_context()

os.makedirs(os.path.join(saveDir), exist_ok=True)
for i, src in enumerate(links):
    if not src:
        continue
    urllib.request.urlretrieve(src, saveDir+"/"+str(i)+".jpg")
    print(i,"saved")