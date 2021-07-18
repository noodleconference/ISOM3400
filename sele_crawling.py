from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E

import time
import pandas as pd

#start chrome
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.openrice.com/en/hongkong/restaurants")
url_district = ['Causeway Bay','Mong Kok','Central','Tsim Sha Tsui','Yuen Long','Tsuen Wan']

#check duplication
def duplicate(name_list, name):
    if name in name_list:
        return True
    else: 
        name_list.append(name)
        return False

#get info
def get_info(bs, info_list, name_list):

    item_list =  bs.find_all('section',class_='content-wrapper')

    #get info of each restaurant
    for item in item_list:
        name = item.find('h2').a.string
        '''
        try:
            price = item.find('div',{'class':'icon-info icon-info-food-price'}).span.string
        except AttributeError:
            price = -1
        
        try:
            bookmark = item.find('div',{'class':'text bookmarkedUserCount js-bookmark-count'}).get("data-count")
        except AttributeError:
            bookmark = -1
            
        try:
            sad = item.find('span',{'class':'score highlight'}).string
        except AttributeError:
            sad = -1
        
        try:
            happy = item.find('span',{'class':'score score-big highlight'}).string
        except AttributeError:
            happy = -1
        
        try:
            food_type = item.find('li').string
        except AttributeError:
            food_type = -1

        try:
            location = item.find('div',{'class':'icon-info address'}).a.string
        except AttributeError:
            location = -1
        '''

        #check duplication
        if not duplicate(name_list,name):
            info_list.append([name])#, price, bookmark, happy, sad, food_type,location])
            print(name)

main_frame = pd.DataFrame({'name':[],'price':[],'bookmark':[],'happy':[],'sad':[],'food_type':[],'location':[]})


for district in url_district:
    search_box = driver.find_element_by_name("where")
    search_box.clear() 
    search_box.send_keys(district,Keys.RETURN)

    info_list = [];name_list = []; endsearch = False
    page = 1
    while not endsearch:
        bs = BeautifulSoup(driver.page_source, 'html.parser')
        bs.prettify()

        get_info(bs, info_list,name_list)

        #go to next page
        '''
        page+=1
        nextpage = driver.find_element_by_link_text(str(page))
        driver.execute_script("arguments[0].click();", element)
        '''
        next_page = bs.find('section', {'class':'js-pois-pagination pull-right'}).find('a',class_='pagination-button next js-next')      
        if next_page == None:
            endsearch = True
        else:
            try:
                print('ok')
                W(driver, 15).until(E.presence_of_element_located((By.LINK_TEXT,'Outdark (飛達商業中心)'))).click()
            except:
                driver.quit()
                break

        
        
    


