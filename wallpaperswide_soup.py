from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import urllib


root = 'http://wallpaperswide.com'
home = requests.get('http://wallpaperswide.com/vintage-desktop-wallpapers.html')
# cats = browser.find_element(By.CSS_SELECTOR, '#left-panel > div.sidebox.categories > div.sidebox-body-r > div > div > div > ul')
# links = cats.find_elements(By.TAG_NAME, 'a')
# cat_addrs = [link.get_attribute('href') for link in links]

soup = BeautifulSoup(home.text, 'html.parser')
cats = soup.select('#left-panel > div.sidebox.categories > div.sidebox-body-r > div > div > div > ul')
links = cats[0].select('a')
cat_addrs = [urljoin(root , link['href']) for link in links]
# print(cat_addrs)

file_count = 0
for cat_addr in cat_addrs:
    print('cat...', cat_addr)
    cur_addr = cat_addr
    
    while True:
        html = requests.get(cur_addr).text
        soup = BeautifulSoup(html, 'html.parser')
        wallpapers = soup.select('#content > .wallpapers')[1]
        links = wallpapers.select('li > div > a')
        
        for link in links[-3:]:
            name = link['href'][:-6]
            addr = f'http://wallpaperswide.com/download/{name}-1920x1080.jpg'
            print(name)
            urllib.request.urlretrieve(addr, f'wallpapers/{name}.jpg')
            
            #limit
            file_count += 1
            if file_count > 500:
                exit()
        
        next = soup.find("a", string="Next »")
        if not next:
            continue
        cur_addr = urljoin(root, next['href'])
        print('next.. ', next['href'])
        

