from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver import ActionChains
import time
import pandas as pd

#start chrome
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.openrice.com/en/hongkong/restaurants")
url_main = 'https://www.openrice.com'
url_district = ['Causeway Bay','Mong Kok','Central','Tsim Sha Tsui','Yuen Long','Tsuen Wan']

#check duplication
def duplicate(name_list, name):
    if name in name_list:
        return True
    else: 
        name_list.append(name)
        return False

#panda data
mainframe = pd.DataFrame({'name':[],'price':[],'bookmark':[],'happy':[],'sad':[],'food_type':[],'location':[]})
def panda_data(oneres):
    addrow = pd.DataFrame([oneres],columns=['name','price','bookmark','happy','sad','food_type','location']) #adding additional row
    global mainframe
    mainframe=mainframe.append(addrow,ignore_index = True)


#get info
def get_info(bs, district):
    global name_list
    item_list =  bs.find_all('section',class_='content-wrapper')

    #get info of each restaurant
    for item in item_list:
        name = item.find('h2').a.string
        
        try:
            price = item.find('div',{'class':'icon-info icon-info-food-price'}).span.string
        except AttributeError:
            continue
        
        try:
            bookmark = item.find('div',{'class':'text bookmarkedUserCount js-bookmark-count'}).get("data-count")
        except AttributeError:
            continue
            
        try:
            sad = item.find('span',{'class':'score highlight'}).string
        except AttributeError:
            continue
        
        try:
            happy = item.find('span',{'class':'score score-big highlight'}).string
        except AttributeError:
            continue
        
        try:
            food_type = item.find('li').string
        except AttributeError:
            continue

        try:
            location = item.find('div',{'class':'icon-info address'}).a.string
            if location != district: continue
        except AttributeError:
            continue
        

        #check duplication
        if not duplicate(name_list,name):
            one_res = [name, price, bookmark, happy, sad, food_type,location]
            panda_data(one_res)

#main
cookie_pressed = False
name_list = []
for district in url_district:
    #find search box
    try:
        search_box = driver.find_element_by_name("where")
        search_box.clear() 
        search_box.send_keys(district)
        search = driver.find_element_by_xpath('//*[@id="header"]/div[2]/div[4]/div/button').click()
        time.sleep(2)
    except:
        print('error'); driver.quit()

    #ready to get info
    endsearch = False; page = 1; info_list = []
    
    while not endsearch:

        bs = BeautifulSoup(driver.page_source, 'html.parser')
        bs.prettify()
        get_info(bs,district)
       
        #go to next page
        #cookies
        try:
            if (page == 1 and not cookie_pressed ):
                print('cookie pressing')
                cookie = W(driver, 2).until(E.presence_of_element_located((By.XPATH,'//*[@id="cookies-agreement"]/div/button')))
                type(cookie)
                cookie.click()
                cookie_pressed = True
                #driver.implicitly_wait(5)
        except:
            print("no cookies")

        # find the link of next page 
        try:
            nextpage = W(driver, 5).until(E.presence_of_element_located((By.LINK_TEXT,str(page))))
            actions = ActionChains(driver)
            actions.move_to_element(nextpage).perform()
        except:
            endsearch = True
            break
       #click on next page
        if not nextpage:
            endsearch = True
        else:
            page +=1
            nextpage.click()
            time.sleep(2)

    print('done',district)

driver.quit()

#dataframe to excel

mainframe.to_excel('restaurant_info_6Districts.xlsx',sheet_name='restaurant info')
        
