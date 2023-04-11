# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:15:37 2023

@author: Yusuke
"""

from bs4 import BeautifulSoup
import pandas as pd
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests

myHeaders = {'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def fetch_url(url):
    # 創建 session
    session = requests.Session()

    # 設置重試策略
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=2
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # 發送請求
    response = session.get(url)
    response.encoding = 'utf-8'

    # 檢查是否成功
    if response.status_code == 200:
        html = requests.get(url).content
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find_all('div', class_='DGPK-SC-SS')
        
        df_list = []
        for t in table:
            df = pd.read_html(str(t))[0]
            df_list.append(df)
        
        print(df_list)
    else:
        raise Exception("Failed to fetch url")
        
url = 'http://twbsball.dils.tku.edu.tw/wiki/index.php/2023%E5%B9%B4%E7%AC%AC%E4%BA%94%E5%B1%86%E4%B8%96%E7%95%8C%E6%A3%92%E7%90%83%E7%B6%93%E5%85%B8%E8%B3%BD'
fetch_url(url)