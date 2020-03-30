from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#global variables
#create a list to store the scraped data
scraped_data = []
newsoup = None

def get_restaurant_yelp_link():
    yelp_link = [] #list of yelp link for each yelp restaurant 
    for i in range(0,60,30):
        URL = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Boston%2C%20MA&start="+str(i)
        #print(type(URL))
        page = requests.get(URL, timeout = 25)
        soup = BeautifulSoup(page.content, 'html.parser')   
        #find all the links to yelp page
        #gets link for each restaurant in the list  
        for link in soup.select('h4 span a'):
            #filters out the ads
            if re.match('^/biz',str(link['href'])):
                yelp_link.append("https://yelp.com"+str(link['href']))
    return yelp_link

def get_amenities():
    amenities = []
    a = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
    for amenity in a:
        amenities.append(amenity.text)
        print (amenities)
    return amenities

def create_dict(yelplink_list):
    global scraped_data
    global newsoup
    #looping through each restaurant url from list
    for yelp_url in yelplink_list:
        #initialize dictionary
        dict = {}

        newpage = requests.get(yelp_url, timeout = 25)
        newsoup = BeautifulSoup(newpage.content, 'html.parser') 


        #get name of restaurant
        try:
            name = newsoup.select('div > div > div:nth-child(1) > h1')[0].text
        except:
            name = "Null"

        #get city
        try: 
            cityname = newsoup.select('address > p:nth-child(2) > span')[0].text
            cityname = cityname.split(',')
            cityname = cityname[0]
            if re.match("^\S+$", cityname):
                city = cityname
        except:
            city = "Null"

        #get star rating 
        try:
            stars= newsoup.find(class_ = re.compile("i-stars--large"))['aria-label']
            stars = str(stars)
            stars = stars.split(' ')
            starrating = stars[0]
        except:
            starrating = "Null"

        #get dollar signs
        try:
            price = newsoup.select('div > div > span:nth-child(3) > span')[0].text
            if re.match("^\$", str(price)):
                pricerange = price
        except:
            pricerange = "Null"

        #get reservation info
        try:
            r = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            for m in r:
                amenities = m.text
                if re.findall("Takes Reservation",str(amenities)):
                    reserve = amenities
                    reserve = reserve.split('\xa0')
                    reserve = reserve[-1]
                    if re.match('^Yes|No|$', reserve) or re.match('^Yes|No|$',reserve):
                        reservation = reserve

        except:
            reservation = "Null"
        
        #get vegan option info
        try:
            v = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            for m in v:
                amenities = m.text
                if re.findall("Vegan Option",str(amenities)):
                    veg = amenities
                    veg = veg.split('\xa0')
                    veg = veg[-1]
                    if re.match('^Yes|No|$', veg) or re.match('^Yes|No|$', veg):
                        vegan = veg

        except:     
            vegan = "Null"

        #get delivery information
        try:
            d = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            for m in d:
                amenities = m.text
                if re.findall("Offers delivery",str(amenities)):
                    deliv = amenities
                    deliv = deliv.split('\xa0')
                    deliv = deliv[-1]
                    if re.match('^Yes|No|$', deliv) or re.match('^Yes|No|$', deliv):
                        delivery= deliv

            # for each in amenities:
            #     if re.findall("Offers delivery",str(each)):
            #         deliv = each.split('\xa0')[-1]
            #         if re.match('^Yes|No|$', deliv) or re.match('^Yes|No|$', deliv):
            #             delivery= deliv

        except:
            delivery = "Null"
    
        #get website of restaurant
        try:
            restwebsite = newsoup.select('div > div > p:nth-child(2) > a')[0].text
        except:
            restwebsite = "Null"

        #get cusine type of restaurant 
        try:
            c = []
            ctype = newsoup.select("div > div > span > span > a")
            for a in ctype:
                c.append(a.text)
            cusine = ', '.join(map(str,c))
            cusinetype = cusine
                
        except:
            cusinetype = "Null"

        #get monday hours
        try:
            mondayhours = newsoup.select('tbody > tr:nth-child(1)>td:nth-child(2)')[0].text
        except:
            mondayhours = "Null"
        
        #get tuesday hours
        try:
            tuesdayhours = newsoup.select('tbody > tr:nth-child(2)>td:nth-child(2)')[0].text
        except:
            tuesdayhours = "Null"
        

        #get wednesday hours
        try:
            wednesdayhours = newsoup.select('tbody > tr:nth-child(3)>td:nth-child(2)')[0].text
        except:
            wednesdayhours = "Null"
        
        #get thursday hours
        try:
            thursdayhours = newsoup.select('tbody > tr:nth-child(4)>td:nth-child(2)')[0].text
        except:
            thursdayhours = "Null"

        #get friday hours
        try:
            fridayhours = newsoup.select('tbody > tr:nth-child(5)>td:nth-child(2)')[0].text
        except:
            fridayhours = "Null"
        

        #get wednesday hours
        try:
            saturdayhours = newsoup.select('tbody > tr:nth-child(6)>td:nth-child(2)')[0].text
        except:
            saturdayhours = "Null"
        
        #get thursday hours
        try:
            sundayhours = newsoup.select('tbody > tr:nth-child(7)>td:nth-child(2)')[0].text
        except:
            sundayhours = "Null"


        #get popular dishes
        try:
            dish_list = []
            popular_list =[]

            #looks for popular dishes
            p = newsoup.find_all('p', class_ = re.compile("lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text--truncated__373c0__3IHqb"))
            #appends to popular dish list 
            for dish in p:
                popular_list.append(dish.text)
            

            #looks for restaurant menu
            m = newsoup.select("div > div:nth-child(4) > div > div.lemon--div__373c0__1mboc.arrange-unit__373c0__1piwO.arrange-unit-fill__373c0__17z0h.border-color--default__373c0__2oFDT > p > a")[0]
            menuURL = "https://yelp.com"+ m['href']
            menupage = requests.get(menuURL, timeout = 25)
            menusoup = BeautifulSoup(menupage.content, 'html.parser') 
            #appends to menu list 
            dish = menusoup.select("h4")
            for d in dish:
                #print(d.text.strip())
                dish_list.append(d.text.strip())

            #gets all the dishes on the menu
            menudish = ', '.join(map(str,dish_list))
            #print(menudish)
            dishes = menudish



            #check if dish is popular
            popular = []
            for menu_item in dish_list:
                if menu_item in popular_list:
                    #print ("exists")
                    popular.append("yes")
                else:
                    #print("not exist")
                    popular.append("no")


        except:
            dishes = "Null"
            

        #add data to the dictionary
        dict['restaurant_name'] = name
        dict['city'] = city
        dict['star_rating'] = starrating
        dict['pricerange'] = pricerange
        dict['reservation'] = reservation
        dict['vegan_option'] = vegan
        dict['delivery_option'] = delivery
        dict['restaurant_website'] = restwebsite
        dict['cusine_types'] = cusinetype
        dict['monday_hours'] = mondayhours
        dict['tuesday_hours'] = tuesdayhours
        dict['wednesday_hours']=wednesdayhours
        dict['thursday_hours'] = thursdayhours
        dict['friday_hours'] = fridayhours
        dict['saturday_hours'] = saturdayhours
        dict['sunday_hours'] = sundayhours
        dict['menu_dishes'] = dishes

        #append the scraped data to the list
        scraped_data.append(dict)
    #return dict

if __name__ == "__main__":
    restaurant_yelp_link = get_restaurant_yelp_link()
    create_dict(restaurant_yelp_link)

    dataFrame = pd.DataFrame.from_dict(scraped_data)
    dataFrame.to_csv('restaurant_data.csv',index = False)



