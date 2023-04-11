# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:49:17 2023

@author: USER
"""

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import csv
import os
import datetime
current_year = datetime.datetime.now().year

def writeCsv(filename, dataList, rosterName, teamName):
    # 如果檔案不存在，則建立檔案並寫入標題列
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([teamName])
            writer.writerow(['---------------'])
    
    # 開啟 CSV 檔案，以附加模式寫入資料
    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([rosterName])
        for row in dataList:
            writer.writerow(row)
            
# reversed_name_list = []
# for name in names[index]: # 把日本選手的英文姓氏與名字反轉
#     reversed_name = name.split()[1] + ", " + name.split()[0]
#     reversed_name_list.append(reversed_name)
# print(reversed_name_list)

driver = webdriver.Chrome()
# options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=93.115.28.181:36138')
# driver = webdriver.Chrome(options=options)
driver.get('https://www.google.com/') # 從google搜尋尋找npb選手資料
try:
    search = driver.find_element(By.NAME, 'q')
    teamName = 'Japan'
    # rosterName = 'Okamoto, Kazuma'
    rosterName = 'Ryoji Kuribayashi'
    search.send_keys(rosterName+' NPB')
    search.send_keys(Keys.ENTER)

    items = driver.find_elements(By.CLASS_NAME, "LC20lb")
    addrs = driver.find_elements(By.CLASS_NAME, "yuRUbf")
   
    for item in zip(items, addrs):
        addr = item[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
        # print(addr)
        if addr[:31] == 'https://npb.jp/bis/eng/players/' and addr[32:39].isdigit(): # 進入npb網站查詢選手資料
            # print(addr)
            driver.get(addr)
            WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'contents')))
            soup = BeautifulSoup(driver.page_source,'html.parser')
            position = soup.find('th', text='Position').find_next_sibling('td').text.strip()
            # print(position)
            if position == 'Pitcher':
                grade_pitch = soup.select('tr.registerStats')
                dataForm = ['Year', 'Team', 'G', 'W', 'L', 'SV', 'HLD', 'HP', 'CG', 'SHO', 'PCT', 'BF', 'IP', 'H', 'HR', 'BB', 'HB', 'SO', 'WP', 'BK', 'R', 'ER', 'ERA', '']
                pitcherList = [dataForm]
                try:
                    for n1 in grade_pitch:
                        n1data = n1.text
                        n1List = n1data.split('\n')
                        n1List[-2] = n1List[-2].strip() # 把n1List[-2]的空白刪除
                        
                        season = int(n1List[1])
                        # 三年內但不包含今年的資料
                        if current_year - season <= 3 and current_year - season > 0:
                            pitcherList.append(n1List[1:])
                    
                    pitcherList_clean = []
                    for row in pitcherList: # 將空串列刪除
                        new_row = []
                        for val in row:
                            if val != '':
                                new_row.append(val)
                        pitcherList_clean.append(new_row)
                    
                    for row_2 in pitcherList_clean: # 將有小數點的欄位融合到上個欄位
                        if '.' in row_2[13]:
                            row_2[12] = row_2[12] + row_2[13]
                            row_2.pop(13)
  
                    if len(pitcherList_clean) == 1:
                        print("沒有最近3年資料")
                    else:
                        print(pitcherList_clean)
                    writeCsv('pitcherlist.csv', pitcherList_clean, rosterName, teamName)
                    break
                    
                except: # 在日職尚無成績
                    print('無美日職棒投球資料')

            else:
                grade_bat = soup.select('table#tablefix_b tr')[1:-1]
                dataForm = ['Year', 'Team', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'TB', 'RBI', 'SB', 'CS', 'SH', 'SF', 'BB', 'HP', 'SO', 'GDP', 'AVG', 'SLG', 'OBP', '']
                hitterList = [dataForm]
                try:
                    for n1 in grade_bat:
                        n1data = n1.text
                        n1List = n1data.split('\n')
                        season = int(n1List[1])
                        # 三年內但不包含今年的資料
                        if current_year - season <= 3 and current_year - season > 0:
                            hitterList.append(n1List[1:])

                    for row_b in hitterList: # 刪除最後一格欄位
                        row_b.pop(-1)
                        
                    if len(hitterList) == 1:
                        print("沒有最近3年資料")
                    else:
                        print(hitterList)
                    writeCsv('hitterList.csv', hitterList, rosterName, teamName)
                    break
                
                except: # 在日職尚無成績
                    print('無美日職棒打擊資料')
                
        else:
            print('無美日職棒資料')
except NoSuchElementException:
    print('無法定位')

# # 從0跑迴圈到999999篩出日職球員資料
# npbUrl = 'https://npb.jp/bis/eng/players/'
# for i in range(51355150,51355154):
#     n_str = str(i).zfill(8)
#     ans = browser.get(npbUrl+n_str+'.html')
#     soup = BeautifulSoup(browser.page_source,'html.parser')
#     data = soup.select('li#pc_v_name')
#     if data:
#         print(data)

sleep(1)
driver.close()