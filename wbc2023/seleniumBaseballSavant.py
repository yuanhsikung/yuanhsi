# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 04:17:50 2023

@author: Yusuke
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep

url = 'https://baseballsavant.mlb.com/' 


browser = webdriver.Chrome()
word = 'Shohei Ohtani'
All_data=[]

browser.get(url)
keyword=browser.find_element(By.ID,'player-auto-complete')
keyword.send_keys(word)
html=browser.find_element(By.TAG_NAME, 'input')
sleep(2)
html.send_keys(Keys.ENTER)

botton = browser.find_element(By.ID,'tab_career')
botton.click()
sleep(2)

soup = BeautifulSoup(browser.page_source,'html.parser')
select_title = soup.select('tr#pitchingStandard-tr_0')

for title in select_title:
    print(title.text, sep=' ')
    
sleep(5)
browser.close()