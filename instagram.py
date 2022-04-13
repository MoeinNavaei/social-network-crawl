
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from sqlalchemy import create_engine

all_data = pd.DataFrame()
driver = webdriver.Chrome(executable_path= r'E:\python codes\VOD\chromedriver.exe')
driver.get('https://instagram.com')
time.sleep(3)
s = driver.find_element_by_name('username')
s.send_keys('farhadmohseni952864@gmail.com')
ss = driver.find_element_by_name('password')
ss.send_keys('Farhadmohseni13579')
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').send_keys(Keys.ENTER)
time.sleep(10)
search = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
#search = driver.find_element_by_xpath('//input[@aria-label="Search Input"')
time.sleep(2)
search.send_keys('#علی_دایی')
search.send_keys(Keys.ENTER)
time.sleep(2)
search.send_keys(Keys.ENTER)
time.sleep(2)
search.send_keys(Keys.ENTER)

a1 = 1
a2 = 0
delay_time = 1
k = 0
def aaa(k, all_data):
    for ii in driver.find_elements_by_tag_name("a"):
#        print(k)
        link = ii.get_attribute('href')
        if '/p/' in link:
            all_data.loc[k, 'link'] = link
            k = k + 1
    all_data.drop_duplicates(subset =['link'], keep = 'last', inplace = True)
    print("len_all_data: ", len(all_data))
    all_data = all_data.reset_index()
    del all_data['index']
    a1 = len(all_data)
    return k, all_data, a1
            
for i in range(2000):
    print("i :", i)
    delta = a1 - a2
    if delta == 0:
        delay_time = delay_time + 1
        if delay_time == 5:
            print('***** STOP PROGRAM *****')
#            time.sleep(30)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight-2000);")
            time.sleep(5)
            delay_time = 1
    a2 = len(all_data)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    [k, all_data, a1] = aaa(k, all_data)
    if len(all_data) > 20000:
        break
    start = time.time()
print("--- %s min (event) ---" % round((time.time() - start)/60, 2))


all_data = all_data.reset_index()
del all_data['index']

#######################################################
driver = webdriver.Chrome(executable_path= r'E:\python codes\VOD\chromedriver.exe')
driver.get('https://telewebion.com/')
time.sleep(20)

#print(i)
driver.execute_script("window.scrollTo(0, 1000)")
time.sleep(5)
driver.execute_script("window.scrollTo(1000, 2000)")
time.sleep(5)
driver.execute_script("window.scrollTo(2000, 3000)")
time.sleep(5)
driver.execute_script("window.scrollTo(3000, 4000)")
time.sleep(5)
driver.execute_script("window.scrollTo(4000, document.body.scrollHeight)")
time.sleep(5)


#print(i)
driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight-1000)")
time.sleep(5)  
driver.execute_script("window.scrollTo(document.body.scrollHeight-1000, document.body.scrollHeight-2000)")
time.sleep(5)    
    

#######################################################
time.sleep(15)
last_height = driver.execute_script("return document.body.scrollHeight")

k = 0
while True:
    for ii in driver.find_elements_by_tag_name("a"):
        print(k)
        link = ii.get_attribute('href')
        if '/p/' in link:
            all_data.loc[k, 'link'] = link
            k = k + 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)
    new_height = driver.execute_script("return document.body.scrollHeight")
#    print(new_height)
    if new_height == last_height:
        break
    last_height = new_height

all_data.drop_duplicates(subset =['link'], keep = 'last', inplace = True)
all_data = all_data.reset_index()
del all_data['index']
#print(all_data.loc[49, 'link'])

###################################################
all_data.insert(1, 'post', '')
all_data.insert(2, 'view', '')
all_data.insert(3, 'total_comments', '')
all_data.insert(4, 'comment', '')

start = time.time()

driver = webdriver.Chrome(executable_path= r'E:\python codes\VOD\chromedriver.exe')
driver.get('https://instagram.com')
time.sleep(3)
s = driver.find_element_by_name('username')
s.send_keys('farhadmohseni952864@gmail.com')
ss = driver.find_element_by_name('password')
ss.send_keys('Farhadmohseni13579')
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').send_keys(Keys.ENTER)
time.sleep(6)

for i in range(984, len(all_data)):   #len(all_data)
    link_post = all_data.loc[i, 'link']
    print(i)
    print(link_post)
    driver.get(link_post)
    time.sleep(3)
    all_comments = ''
    total_comments = ''
    count_comments = 1
    try:
        post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span')
#        print(post.text)
        all_data.loc[i, 'post'] = post.text
    except: pass
    try:
        view = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div')
#        print(view.text)
        all_data.loc[i, 'view'] = view.text
    except: pass
    try:
        total_comments = len(driver.find_elements_by_class_name('Mr508 '))
        all_data.loc[i, 'total_comments'] = total_comments
        for d in range(total_comments):
            comment = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/ul[{}]/div/li/div/div/div[2]/span'.format(count_comments))
            all_comments = all_comments + '-----' + comment.text
            count_comments = count_comments + 1
        all_data.loc[i, 'comment'] = all_comments
    except: pass
print("--- %s min (duration) ---" % round((time.time() - start)/60, 2))

all_data.to_excel('all_data.xlsx', index=False)

#engine = create_engine('postgresql://postgres:12344321@10.32.141.17/Moein01',pool_size=20, max_overflow=100,)
#con=engine.connect()
#all_data.to_sql('Instagram',con,if_exists='replace', index=False)
#con.close()

print(all_data.loc[600, 'link'])


#try:
#    all_data.loc[0, 'user'] = driver.find_element_by_xpath('//h2[@class="_7UhW9       fKFbl yUEEX   KV-D4              fDxYl     "]').text
#    print('11')
#except: pass
#
#try:
#    all_data.loc[0, 'post'] = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[1]').text
#    print('22')
#except: pass
#try:
#    all_data.loc[0, 'followers'] = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]').text
#    print('33')
#except: pass
#try:
#    all_data.loc[0, 'following'] = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[3]').text
#    print('44')
#except: pass
#
#try:
#    all_data.loc[0, 'name'] = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/div[2]/h1').text
#    print('55')
#except: pass
#
#try:
#    all_data.loc[0, 'name1'] = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/section/main/div/header/section/div[2]').text
#    print('66')
#except: pass

















