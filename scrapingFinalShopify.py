
import pandas as pd
import urllib.request
import time
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from PIL import Image
import requests
from io import BytesIO



def openbrowser(): 
 options = webdriver.ChromeOptions()

 options.add_argument('--ignore-certificate-errors')
 prefs = {
  "translate_whitelists": {"id":"en"},
  "translate":{"enabled":"true"}
 }
 options.add_experimental_option("prefs", prefs)
 options.add_argument('--headless')
 options.add_argument('--headless')
 options.add_argument('--no-sandbox')
 #  options.add_argument('--disable-dev-shm-usage')
 driver = webdriver.Chrome( "chromedriver",options=options)
 # driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
 driver.delete_all_cookies()
 return driver

def scrappingpage(i,driver):
 imagelink=[]
 header=[]
 validities=[] 
 time.sleep(2) 
 driver.get(f"https://shopee.co.id/campaigns/?category=0&page={i}")
 time.sleep(10)   
 actions = ActionChains(driver)
 actions.send_keys(Keys.ARROW_DOWN)
 j=1
 while j<50:
        actions.perform()
        content=driver.page_source
        j=j+1
 time.sleep(10)       
    
 soup = BeautifulSoup(content,"html.parser")
 for a in soup.findAll('div', attrs={'class':'campaign-item'}):
    g=a.find('div',attrs={'class':'campaign-item__top'})
    h=g.find('img')
    print(h)
    image='abcd'
    image=h.get('src')
    print(image)
    
   
    imagelink.append(image)
    fontheader=a.find('h2',attrs={'class':'campaign-item__title'}).text
    header.append(fontheader)
    validity=a.find('div',attrs={'class':'campaign-item__expiry'}).text
    validities.append(validity)
    time.sleep(2)
 driver.quit()
 return imagelink,header,validities
 


def access(arr, attr):
    try:
        return arr[attr]
    except Exception as e:
        print(e)
        time.sleep(2)
        return access(arr, attr)
        


# In[28]:
def scrapingfoodcoupons():
 imagesscrapped=[]
 imagelink=[]
 headers=[]
 validitiess=[]
 time.sleep(5)
 i=1
 j=1
 while i<=1:
   driver=openbrowser()   
   imagelink,header,validities=scrappingpage(i,driver)
   imagesscrapped.extend(imagelink)
   headers.extend(header)
   validitiess.extend(validities)
   print(len(imagesscrapped))
   i=i+1
  # print('lalalalall')
   time.sleep(2)

 dictionary={'imageUrls':imagesscrapped,'title':headers,'validity':validitiess}
 df=pd.DataFrame(dictionary)
 df.to_csv('scrappeddatashopify.csv',index=False)
 for url in imagesscrapped:
   if url is not None: 
    response = requests.get(url)
    image=Image.open(BytesIO(response.content))
    path=f"/content/drive/My Drive/text-detection-ctpn/data/demo/image{j}.jpeg"
    print(path)
    image.convert('RGB').save(path)   
    j=j+1
    print(j)
   
 return imagesscrapped
 


