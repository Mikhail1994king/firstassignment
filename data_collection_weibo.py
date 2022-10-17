from typing_extensions import Self
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os.path
import time
import urllib.request
from datetime import datetime, timedelta
from collections import defaultdict
from snownlp import SnowNLP 
import numpy as np
import statistics
import time
import json
import streamlit as st
from selenium.webdriver.chrome.options import Options


base="dark"
primaryColor="purple"

chrome_options = Options()
chrome_options.add_argument('--dns-prefetch-disable')


link = "https://accounts.google.com"




#import streamlit as st

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications");
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=(r"chromedriver"), options = chrome_options)



now = datetime.now()
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')

buzzword = ""

URL = f"https://weibo.com/login.php"
driver.get(URL)

# Wait for the menu element
wait_for_element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'layer_menu_list')) #This is a dummy element
)

feeds_dict = defaultdict(list)
sentiment_dict = defaultdict(list)

current = now

buzzword = "台湾"

for i in range(1, 10):
    time.sleep(3)
    s = []
    d_plus_one = current.strftime('%Y-%m-%d')
    current = current - timedelta(days=1)
    d = current.strftime('%Y-%m-%d')
    try:
        URL = f"https://s.weibo.com/weibo?q={urllib.parse.quote(buzzword)}&xsort=hot&suball=1&timescope=custom:{d}:{d_plus_one}:&Refer=g"
        driver.get(URL)
        # Wait for the card-feed element
        wait_for_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card-feed')) #This is a dummy element
        )
        # Find all feeds on main page
        feeds_cards = driver.find_elements(By.CLASS_NAME, 'card-feed')
        # collect and store under ID
        for feed in feeds_cards:
            feed_text = feed.find_element(By.CLASS_NAME, 'txt').text
            #feed_author = feed.find_element(By.CLASS_NAME, 'name').text
            feeds_dict[d].append(feed_text)
            s.append(SnowNLP(feed_text).sentiments)  
    except:
        pass
    sentiment_dict[d] = statistics.mean(s)


with open(r"mike.json", "w") as outfile:
    json.dump(feeds_dict, outfile)

driver.quit()

print(feeds_dict)

show = pd.DataFrame.from_dict([sentiment_dict]).transpose()
show.columns = ["Weibo"]

st.header('Analysis of 台灣 sentiment in Weibo')
st.line_chart(show)




df=pd.DataFrame(show)
df2 = pd.DataFrame.from_dict(feeds_dict, orient='index').transpose()

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

@st.cache
def convert_df(df2):
   return df2.to_csv().encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Press to Download the extracted data",
   csv,
   "file.csv",
   "text/csv",
   key='download1-csv',
)

csv2 = convert_df(df2)

st.download_button(
   "Press to Download the sentiment analysis",
   csv2,
   "file.csv",
   "text/csv",
   key='download2-csv',
)


st.balloons()

