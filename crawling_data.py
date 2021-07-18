import requests
from bs4 import BeautifulSoup
import openpyxl

user_header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


# prepare url
url_main = 'https://www.openrice.com'
start_url = 'https://www.openrice.com/en/hongkong/restaurants/district/'
url_district = ['causeway-bay','mong-kok','central','tsim-sha-tsui','yuen-long','tsuen-wan']


#write to excel

def excel(info_list):
    local_path=r'c:\Users\Chan Kin Yan\Desktop\ZOE\BUSI\ISOM\ISOM3400\project\restaurants.xlsx'
    wb = openpyxl.load_workbook(local_path)
    sheet = wb.active; sheet.title = "restaurant_info"
    sheet.append(['name', 'price', 'bookmark', 'happy', 'sad', 'food_type','location'])
    for i in info_list:
        sheet.append(i)
    wb.save(local_path)


#check duplication
def duplicate(name_list, name):
    if name in name_list:
        return True
    else: 
        name_list.append(name)
        return False


# get infomation for page restauant 
def get_info(url,info_list):
    res = requests.get(url,headers = user_header)
    bs = BeautifulSoup(res.text, 'html.parser')
    bs.prettify()
    item_list =  bs.find_all('section',class_='content-wrapper')

    #get info of each restaurant
    for item in item_list:
        name = item.find('h2').a.string
        
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
        

        #check duplication
        if not duplicate(name_list,name):
            info_list.append([name, price, bookmark, happy, sad, food_type,location])

    # check to get url of next page
    next_page = bs.find('section', {'class':'js-pois-pagination pull-right'}).find('a',class_='pagination-button next js-next')      
    if next_page == None:
        return None
    else:
        next_page = next_page.attrs['href']
        url=url_main+str(next_page)
        return url

# main 

for district in url_district:
    url = start_url+district #each district url
    info_list = []
    name_list=[] # use for checking duplacted restaurant

    while url:
        #get info of each page
        url = get_info(url,info_list)

    excel(info_list)
    