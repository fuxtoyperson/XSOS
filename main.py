#!/usr/bin/env python
# coding: utf-8

# In[44]:


import requests as rq
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
today = date.today()


# In[45]:


def dicname(name):
    if name in ['online','buy123','eslite','i3fresh','hahow']:
        if name == 'online':
            return "家樂福線上購物"
        elif name == "buy123":
            return "生活市集"
        elif name == "eslite":
            return "誠品線上"
        elif name == "i3fresh":
            return "愛上新鮮i3Fresh"
        elif name == "hahow":
            return "Hahow"  
    else : return name
def getlinepayweb():
    aurl = 'https://www.shopback.com.tw/ctbc-line-pay'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    aresp = rq.get(aurl) # 用 requests 的 get 方法把網頁抓下來
    aresp.encoding='utf8'
    soup = BeautifulSoup(aresp.text, 'html.parser')
    deal = soup.find_all('a', attrs={'class': "ctbc__deal"})
    deal = str(deal).split(' ')
    for i in range(len(deal)):
        if deal[i].startswith('href='):
            ans = deal[i].split("/")[3]
            url_list.append(ans.split('"')[0]) 
def connect_url(url):
    resp = rq.get(url) 
    resp.encoding='utf8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    div_2 = soup.find_all('section', attrs={'class': 'py-3 px-4 border border-sb-white shadow-md bg-sb-white-two border-solid rounded'})[0]
    data = div_2.text
    data = data.split("0.00%")
    while '' in data:
        data.remove('')
    return data
#client = MongoClient("mongodb+srv://timtim:timtim@cluster0.4itfxce.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient("mongodb+srv://timmy:timmy@cluster.gq4ybub.mongodb.net/?retryWrites=true&w=majority")

mydb = client['XSOS']
mycol = mydb['XSOS']


# In[46]:


url_list=[]
getlinepayweb()
json_array =[]
print(today)
for num in range(len(url_list)):
    crawl_url = 'https://www.shopback.com.tw/'+url_list[num]
    crawl_name = url_list[num].split("-")[0]
    crawl_name = dicname(crawl_name)
    ans = connect_url(crawl_url)
    json_body = {
        'date': str(today),
        'name': crawl_name,
        'commission':ans,
        
    }
    json_array.append(json_body)


# In[50]:


mycol.insert_many(json_array)

