# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:09:45 2023

@author: Yusuke
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
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
    
def advStatsMLB(hitStatsMLB):
    for i in hitStatsMLB:
        print(hitStatsMLB[i])
        # obp = 
        # iso = #(純長打率)
        # fip #(投手獨立防禦)
        # whip #(每局上壘率)
        # k/9 = #(每9局三振率)
        # hr/9 = #(每9局全壘打數)
        # k/bb =  #(三振四壞率)
        # # ELO(等級分)
        # # 休息間距


    
    
def pitcherMLB(rosterName, teamName):
    tag_pitch = driver.find_element(By.ID,'stats_nav_type_pitching')
    tag_pitch.click()
    soup = BeautifulSoup(driver.page_source,'html.parser')
    grade_pitch = soup.find_all('tr', id=re.compile('pitchingStandard-tr_\d+'))[:-1]
    
    dataForm = ['Season','Tm','LG','BF','W','L','ERA','G','GS','SV','IP','H','R','ER','HR','BB','SO','WHIP']
    pitchStatsMLB = [dataForm]
    for n1 in grade_pitch:
        n1Data = n1.text
        n1List = n1Data.split(' ')
        season = int(n1List[2])
        # 三年內但不包含今年的資料
        if current_year - season <= 3 and current_year - season > 0 and n1List[4] != 'Teams':
            pitchStatsMLB.append(n1List[2:])
    if len(pitchStatsMLB) == 1: # 若在大聯盟沒資料，一樣跳去查日職
        npbSearch(rosterName, teamName) 
    else:
        try:
            from tabulate import tabulate
            print(tabulate(pitchStatsMLB, headers='firstrow', tablefmt='fancy_grid'))
        except ModuleNotFoundError:
            print(pitchStatsMLB)
        # advStatsMLB(pitchStatsMLB)
    writeCsv('pitchStatsMLB.csv', pitchStatsMLB, rosterName, teamName)
    
def batterMLB(rosterName, teamName):
    tag_bat = driver.find_element(By.ID,'stats_nav_type_batting')
    tag_bat.click()
    soup = BeautifulSoup(driver.page_source,'html.parser')
    grade_bat = soup.find_all('tr', id=re.compile('hittingStandard-tr_\d+'))[:-1]
    
    dataForm = ['Season','Tm','LG','G','PA','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','HBP','AVG','OBP','SLG','OPS']
    hitStatsMLB = [dataForm]
    for n1 in grade_bat:
        n1Data = n1.text
        n1List = n1Data.split(' ')
        try: # 因為會爬到進階打擊數據，所以用n1List[2]爬到的數據比對不是數字就換下個球員
            season = int(n1List[2])
            # 三年內但不包含今年的資料
            if current_year - season <= 3 and current_year - season > 0:
                if n1List[4] != 'Teams':
                    hitStatsMLB.append(n1List[2:])
        except ValueError:
            pass
    if len(hitStatsMLB) == 1:
        print("沒有最近3年資料")
    else:
        try:
            from tabulate import tabulate
            print(tabulate(hitStatsMLB, headers='firstrow', tablefmt='fancy_grid'))
        except ModuleNotFoundError:
            print(hitStatsMLB)
        # advStatsMLB(hitStatsMLB)
    writeCsv('hitStatsMLB.csv', hitStatsMLB, rosterName, teamName)
        
            
def picherOrNot_Milb(rosterName, teamName): # 小聯盟_選手守備位置是否為投手
    print(rosterName+' (Milb)')
    current_url = driver.current_url
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    position = soup.find('div', {'style': 'font-size: .8rem;'}).text.strip()[:1]
    # print(position)
    if position == 'P':
        tag_pitch = driver.find_element(By.ID,'stats_nav_type_pitching') # 點進PITCHING區塊
        tag_pitch.click()
        soup = BeautifulSoup(driver.page_source,'html.parser')
        grade_pitch = soup.select('tr.default-table-row:not(.footer-class.static)[id^="pitchingStandardMiLB-tr_"]')
        dataForm = ['Season','Tm','LG','L','W','L','ERA','G','GS','SV','IP','H','R','ER','HR','BB','SO','WHIP']
        pitchStatsMiLB = [dataForm]
        for n1 in grade_pitch:
            n1Data = n1.text
            n1List = n1Data.split(' ')
            oFL = len(n1List) - 18 # 小聯盟投球資料有18個欄位，Tm保留1個欄位
            # print(oFL)
            if oFL == 3: # 表示Tm欄位多佔2個欄位+第一欄空值
                n1List[2] = n1List[2] + ' ' + n1List[3] + ' ' + n1List[4]
                # print(n1List[2])
                for i in range(2, 2+oFL-1): #(2,4)
                    n1List.pop(6-i)
                # print(n1List)
            elif oFL == 2:
                n1List[2] = n1List[2] + ' ' + n1List[3]
                # print(n1List[2])
                for i in range(2, 2+oFL-1): #(2,3)
                    n1List.pop(5-i)
                # print(n1List)
            season = int(n1List[1])
            # 三年內但不包含今年的資料
            if current_year - season <= 3 and current_year - season > 0:
                pitchStatsMiLB.append(n1List[1:])
        if len(pitchStatsMiLB) == 1:
            print("沒有最近3年資料")
        else:
            try:
                from tabulate import tabulate
                print(tabulate(pitchStatsMiLB, headers='firstrow', tablefmt='fancy_grid'))
            except ModuleNotFoundError:
                print(pitchStatsMiLB)
        writeCsv('pitchStatsMiLB.csv', pitchStatsMiLB, rosterName, teamName)
        
    else:    
        tag_bat = driver.find_element(By.ID,'stats_nav_type_batting') # 點進BATTING區塊
        tag_bat.click()
        soup = BeautifulSoup(driver.page_source,'html.parser')
        # grade_bat = soup.find_all('tr', id=re.compile('hittingStandardMiLB-tr_\d+'))[-4:-1]
        grade_bat = soup.select('tr.default-table-row:not(.footer-class.static)[id^="pitchingStandardMiLB-tr_"]')
        dataForm = ['Season','Tm','LG','L','G','PA','AB','R','H','2B','3B','HR','RBI','BB','SO','SB','CS','HBP','AVG','OBP','SLG','OPS']
        hitStatsMiLB = [dataForm]
        for n1 in grade_bat:
            n1Data = n1.text
            n1List = n1Data.split(' ')
            oFL = len(n1List) - 22 # 小聯盟打擊資料有22個欄位，Tm保留1個欄位
            # print(oFL)
            if oFL == 3: # 表示Tm欄位多佔2個欄位+第一欄空值
                n1List[2] = n1List[2] + ' ' + n1List[3] + ' ' + n1List[4]
                # print(n1List[2])
                for i in range(2, 2+oFL-1): #(2,4)
                    n1List.pop(6-i)
                # print(n1List)
            elif oFL == 2:
                n1List[2] = n1List[2] + ' ' + n1List[3]
                # print(n1List[2])
                for i in range(2, 2+oFL-1): #(2,3)
                    n1List.pop(5-i)
                # print(n1List)
            season = int(n1List[1])
            # 三年內但不包含今年的資料
            if current_year - season <= 3 and current_year - season > 0:
                hitStatsMiLB.append(n1List[1:])
        if len(hitStatsMiLB) == 1:
            print("沒有最近3年資料")
        else:
            try:
                from tabulate import tabulate
                print(tabulate(hitStatsMiLB, headers='firstrow', tablefmt='fancy_grid'))
            except ModuleNotFoundError:
                print(hitStatsMiLB)
        writeCsv('hitStatsMiLB.csv', hitStatsMiLB, rosterName, teamName)


def npbSearch(rosterName, teamName): # 搜尋日職資料
    driver.get('https://www.google.com/') # 從google搜尋尋找npb選手資料
    try:
        print(rosterName)
        search = driver.find_element(By.NAME, 'q')
        search.send_keys(rosterName+' npb')
        search.send_keys(Keys.ENTER)
    
        items = driver.find_elements(By.CLASS_NAME, "LC20lb")
        addrs = driver.find_elements(By.CLASS_NAME, "yuRUbf")
        
        for item in zip(items, addrs):
            addr = item[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
            count = 0
            if addr[:31] == 'https://npb.jp/bis/eng/players/' and addr[32:39].isdigit(): # 進入npb網站查詢選手資料
                driver.get(addr)
                WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'contents')))
                soup = BeautifulSoup(driver.page_source,'html.parser')
                position = soup.find('th', text='Position').find_next_sibling('td').text.strip()
                # print(position)
                if position == 'Pitcher':
                    grade_pitch = soup.select('tr.registerStats')
                    dataForm = ['Year', 'Team', 'G', 'W', 'L', 'SV', 'HLD', 'HP', 'CG', 'SHO', 'PCT', 'BF', 'IP', 'H', 'HR', 'BB', 'HB', 'SO', 'WP', 'BK', 'R', 'ER', 'ERA', '']
                    pitchStatsAlpha = [dataForm]
                    try:
                        for n1 in grade_pitch:
                            n1data = n1.text
                            n1List = n1data.split('\n')
                            n1List[-2] = n1List[-2].strip() # 把n1List[-2]的空白刪除
                            season = int(n1List[1])
                            # 三年內但不包含今年的資料
                            if current_year - season <= 3 and current_year - season > 0:
                                pitchStatsAlpha.append(n1List[1:])
                                
                        pitchStatsNPB = [] # 開一個新串列把表重新整理
                        for row in pitchStatsAlpha: # 首先將空串列刪除
                            new_row = []
                            for val in row:
                                if val != '':
                                    new_row.append(val)
                            pitchStatsNPB.append(new_row)
                        
                        for row_2 in pitchStatsNPB: # 接著將有小數點的IP(投球局數)欄位接回前一個欄位
                            if '.' in row_2[13]:
                                row_2[12] = row_2[12] + row_2[13]
                                row_2.pop(13)
                        # print(pitchStatsNPB)
                        
                        if len(pitchStatsNPB) == 1:
                            print("沒有最近3年資料")
                        else:
                            try:
                                from tabulate import tabulate
                                print(tabulate(pitchStatsNPB, headers='firstrow', tablefmt='fancy_grid'))
                            except ModuleNotFoundError:
                                print(pitchStatsNPB)
                        writeCsv('pitchStatsNPB.csv', pitchStatsNPB, rosterName, teamName)
                        break
                                        
                    except: # 在日職尚無成績
                        print('無美日職棒投球資料')

                else:
                    grade_bat = soup.select('table#tablefix_b tr')[1:-2]
                    dataForm = ['Year', 'Team', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'TB', 'RBI', 'SB', 'CS', 'SH', 'SF', 'BB', 'HP', 'SO', 'GDP', 'AVG', 'SLG', 'OBP', '']
                    hitStatsNPB = [dataForm]
                    try:
                        for n1 in grade_bat:
                            n1data = n1.text
                            n1List = n1data.split('\n')
                            season = int(n1List[1])
                            # 三年內但不包含今年的資料
                            if current_year - season <= 3 and current_year - season > 0:
                                hitStatsNPB.append(n1List[1:])
                                
                        for row_b in hitStatsNPB: # 刪除最後一格欄位
                            row_b.pop(-1)
                            
                        if len(hitStatsNPB) == 1:
                            print("沒有最近3年資料")
                        else:
                            try:
                                from tabulate import tabulate
                                print(tabulate(hitStatsNPB, headers='firstrow', tablefmt='fancy_grid'))
                            except ModuleNotFoundError:
                                print(hitStatsNPB)
                        writeCsv('hitStatsNPB.csv', hitStatsNPB, rosterName, teamName)
                        break
                    
                    except: # 在日職尚無成績
                        print('無美日職棒打擊資料')

            else:
                count += 1
                if count > 1:
                    print('無美日職棒資料')
                    break
    except NoSuchElementException:
        print('無法定位')

#可以不讓瀏覽器執行在前景，而是在背景執行, 如以下宣告 options
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('--headless')

# teams = ['australia','canada','china','chinese-taipei','colombia','cuba','czech-republic',
#         'dominican-republic','great-britain','israel','italy','japan','kingdom-of-the-netherlands',
#         'korea','mexico','nicaragua','panama','puerto-rico','united-states','venezuela']

# names = ['ausName','caName','cnName','ctName','colName','cubaName','czName',
#         'domName','brName','isName','italyName','jpName','nlName',
#         'koName','mexName','nicName','paName','prName','usName','venName']

# teams = ['japan','united-states','cuba','mexico',]
# names = ['jpName','usName','cubaName','mexName',]

teams = ['cuba','mexico','japan','united-states']
names = ['cubaName','mexName','jpName','usName']

for index, val in enumerate(teams):
    url = 'https://www.mlb.com/world-baseball-classic/roster/'+teams[index] 
    
    driver = webdriver.Chrome(options=ChromeOptions)
    driver.get(url)
    WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'table-cellstyle__StyledTableCell-sc-xpntj7-2.bkvOva')))

    soup = BeautifulSoup(driver.page_source,'html.parser')
    playerNames = soup.select('a.RosterTeamView__PlayerNameLink-sc-n6huj0-2.jFuBmf')
    teamName = teams[index].title()
    print(teamName)
    names[index] = []
    
    for name in playerNames:
        x = name.text
        names[index].append(x)
    print('-----------------')
    # print(names[index])
    # driver.close()
    
    for index2, val2 in enumerate(playerNames): # 填上選手名字
        url_savant = 'https://baseballsavant.mlb.com/' 
    
        driver = webdriver.Chrome(options=ChromeOptions)
        driver.get(url_savant)
        rosterName = names[index][index2]
        # rosterName = 'Erubiel Armenta'
        # rosterName = 'Masataka Yoshida'
        WebDriverWait(driver,5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME,"HeaderAC-MuiInputBase-root")))
        
        while True: # 若輸入名字會跳掉就強制再輸入到有資料為止
            try:
                keyword = driver.find_element(By.ID,'player-auto-complete')
                keyword.send_keys(rosterName)
                value = keyword.get_attribute('value')
                
                if len(value) > 30: # 名字長度過長表示陷入無限迴圈，就中斷迴圈轉到日職查詢
                    break
                    npbSearch(rosterName, teamName)
                sleep(2)
                sumbit = driver.find_element(
                    By.CSS_SELECTOR, 'input#player-auto-complete').send_keys(Keys.ENTER)
                WebDriverWait(driver,5).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR,'div.tab-set')))
                break
            except Exception as e:
                # print(f"An error occurred: {e}")
                pass
        
        try: # 點進STANDARD區塊
            botton = driver.find_element(By.ID,'tab_career')
            botton.click()
        except NoSuchElementException: # 在網站中是否有資料，若無就轉去日職網站搜尋
            npbSearch(rosterName, teamName) 
            
        try: # 大聯盟
            tag = driver.find_element(By.ID,'level_mlb_career').click()
            print(rosterName+' (MLB)')
            # 判斷選手的守備位置是否為投手
            current_url = driver.current_url
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            position = soup.find('div', {'style': 'font-size: .8rem;'}).text.strip()[:1]
            # print(position)
            if position == 'P': # 點進PITCHING區塊
                pitcherMLB(rosterName, teamName)
                    
            elif position == 'T': # 二刀流，點進PITCHING 和 BATTING區塊
                pitcherMLB(rosterName, teamName)
                batterMLB(rosterName, teamName)
                
            else: # 點進BATTING區塊
                batterMLB(rosterName, teamName)
        except NoSuchElementException:
            try: # 小聯盟
                tag = driver.find_element(By.ID,'level_minors_career')
                picherOrNot_Milb(rosterName, teamName) # 判斷選手的守備位置是否為投手
                # print('抱歉，目前不接入小聯盟資料')
                    
            except NoSuchElementException:
                npbSearch(rosterName, teamName) 
                    
                    
        '''
        # 判斷是否有大聯盟成績 (mlb字串 > 700 => 有)       
        count = browser.page_source.count('mlb')
        # print(count)
        if count >= 800: #大聯盟
            botton = browser.find_element(By.ID,'level_mlb_career')
            botton.click()
            soup = BeautifulSoup(browser.page_source,'html.parser')
            
            # 點進PITCHING區塊
            botton = browser.find_element(By.ID,'stats_nav_type_pitching')
            botton.click()
            grade_pitch = soup.select('tr#pitchingStandard-tr_0')
            for grade in grade_pitch:
                print(grade.text)
                
            # 點進BATING區塊
            botton = browser.find_element(By.ID,'stats_nav_type_batting')
            botton.click()
            grade_bat = soup.select('tr#hittingStandard-tr_0')
            for grade in grade_bat:
                print(grade.text)
        elif count < 800 and count >= 400: #小聯盟
            botton = browser.find_element(By.ID,'level_minors_career') 
            botton.click()
            soup = BeautifulSoup(browser.page_source,'html.parser')
            select_title = soup.select('tr#pitchingStandardMiLB-tr_0')
        
            for title in select_title:
                print(title.text)
        elif count < 400: #無美職資料
            print('該選手無美國職棒資料')     
        '''
            
        sleep(2)
        driver.close()













