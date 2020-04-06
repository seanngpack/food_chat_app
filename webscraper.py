from bs4 import BeautifulSoup
import time
import timeit
import pandas as pd
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
from datetime import datetime
import lxml
import urllib.request
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

#global variables
#create a list to store the scraped data
scraped_data = []
test_yelp = []
  
# code snippet whose execution time is to be measured 
def check_if_popular(pop_list, menu_list):
    popular =[]
    for menu_item in menu_list:
        if menu_item in pop_list:
            popular.append("yes")
        else:
            popular.append("no")
    pop_dishes = ', '.join(map(str,popular))
    return pop_dishes

def get_1000_restaurants():
    rest_URL = [] #get list of URL for each page of 30 restaurants
    for i in range(0,60,30):
        URL = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Boston%2C%20MA&start="+str(i)
        rest_URL.append(URL)
    return rest_URL

def try_threading(urlList):
    global test_yelp
    try:
        test_yelp=[]
        page = urllib.request.urlopen(urlList)
        soup = BeautifulSoup(page, 'lxml') 
        for link in soup.find_all('a', class_ = 'lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'):
            #filters out the ads
            if re.match('^/biz',str(link['href'])):
                test_yelp.append("https://yelp.com"+str(link['href']))
    except:
        print("error")

def try_threading_each(test_yelp_url):
    global scraped_data
    dict = {}

    newpage = urllib.request.urlopen(test_yelp_url)
    newsoup = BeautifulSoup(newpage, 'lxml') 
    #get name of restaurant
    try:
        name = newsoup.find('h1', class_ = 'lemon--h1__373c0__2ZHSL heading--h1__373c0__1VUMO heading--no-spacing__373c0__1PzQP heading--inline__373c0__1F-Z6').text
    except:
        name = "Null"

    #get city
    try: 
        cityname = newsoup.select('address > p')[1].text.split(',')[0]
        if re.match("^\S+$", cityname):
            city = cityname
        else:
            cityname = newsoup.select('address > p')[2].text.split(',')[0]
            if re.match("^\S+$", cityname):
                city = cityname
    except:
        city = "Null"

    #get star rating 
    try:
        starrating= newsoup.find(class_ = re.compile("i-stars--large"))['aria-label'].split(' ')[0]
    except:
        starrating = "Null"

    #get dollar signs
    try:
        price =  newsoup.find('span', class_='lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-bullet--after__373c0__1ZHaA text-size--large__373c0__1568g').text
        if re.match("^\$", str(price)):
            pricerange = price
    except:
        pricerange = "Null"

    #get reservation info
    try:
        r = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
        for m in r:
            amenities = m.text
            if re.match("Takes Reservations",str(amenities)):
                reserve = amenities.split('\xa0')[-1]
                if re.match('^Yes|No|$', reserve) or re.match('^Yes|No|$',reserve):
                    reservation = reserve
                    break
            else:
                reservation = "Null"
    except:
        reservation = "Null"

    #get vegan option info
    try:
        for m in r:
            amenities = m.text
            if re.findall("Vegan Option",str(amenities)):
                veg = amenities.split('\xa0')[-1]
                if re.match('^Yes|No|$', veg) or re.match('^Yes|No|$', veg):
                    vegan = veg
                    break
            else:
                vegan = "Null"
    except:     
        vegan = "Null"

    #get delivery information
    try:
        for m in r:
            amenities = m.text
            if re.findall("Offers Delivery",str(amenities)):
                deliv = amenities.split('\xa0')[-1]
                if re.match('^Yes|No|$', deliv) or re.match('^Yes|No|$', deliv):
                    delivery= deliv
                    break
            else:
                delivery = "Null"
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
        c =[a.text for a in ctype]
        cusinetype = ', '.join(map(str,c))             
    except:
        cusinetype = "Null"

    #get monday hours
    try:
        mondayhours = newsoup.select_one('tbody > tr:nth-child(1)>td:nth-child(2)').text
    except:
        mondayhours = "Null"
        
    #get tuesday hours
    try:
        tuesdayhours = newsoup.select_one('tbody > tr:nth-child(2)>td:nth-child(2)').text
    except:
        tuesdayhours = "Null"
        
    #get wednesday hours
    try:
        wednesdayhours = newsoup.select_one('tbody > tr:nth-child(3)>td:nth-child(2)').text
    except:
        wednesdayhours = "Null"
        
    #get thursday hours
    try:
        thursdayhours = newsoup.select_one('tbody > tr:nth-child(4)>td:nth-child(2)').text
    except:
        thursdayhours = "Null"

    #get friday hours
    try:
        fridayhours = newsoup.select_one('tbody > tr:nth-child(5)>td:nth-child(2)').text
    except:
        fridayhours = "Null"
        
    #get saturday hours
    try:
        saturdayhours = newsoup.select_one('tbody > tr:nth-child(6)>td:nth-child(2)').text
    except:
        saturdayhours = "Null"
        
    #get sunday hours
    try:
        sundayhours = newsoup.select_one('tbody > tr:nth-child(7)>td:nth-child(2)').text
    except:
        sundayhours = "Null"
    
    #get popular dishes
    try:
        dish_list = []
        popular_list =[]

        #appends to popular dish list 
        popular_list = [dish.text for dish in newsoup.find_all('p', class_ = re.compile("lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text--truncated__373c0__3IHqb"))]
            
        #looks for restaurant menu
        m = newsoup.select_one("div > div:nth-child(4) > div > div.lemon--div__373c0__1mboc.arrange-unit__373c0__1piwO.arrange-unit-fill__373c0__17z0h.border-color--default__373c0__2oFDT > p > a")
        menuURL = "https://yelp.com"+ m['href']
        menupage = requests.get(menuURL,timeout=1)
        menusoup = BeautifulSoup(menupage.text, 'lxml')

        #appends to menu list
        dish_list=[d.text.strip()for d in menusoup.find_all("h4")]

        #gets all the dishes on the menu
        dishes = ', '.join(map(str,dish_list))
           
        #check if dish is popular
        popular = check_if_popular(popular_list, dish_list)

    except:
        dishes = "Null"
        popular = "Null"

    #get 5 reviews
    try:
        review =[rev.text for rev in newsoup.find_all("p",class_ = 'lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_')]
        if (len(review)<5):
            reviews = '> '.join(map(str,review[0:len(review)]))
        else:
            reviews = '> '.join(map(str,review[0:5]))
    except:
        reviews = "Null"

    #get review star rating
    try:
        reviewstar = [i['aria-label'].split(' ')[0] for i in newsoup.find_all('div', class_=re.compile('i-stars--regular'))]
        if (len(reviewstar) < 5):
            reviewstarrating = ', '.join(map(str,reviewstar[0:len(reviewstar)]))
        else:
            reviewstarrating = ', '.join(map(str,reviewstar[0:5]))
    except:
        reviewstarrating = "Null"

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
    dict['popular_dishes'] = popular
    dict['reviews'] = reviews
    dict['review_rating'] = reviewstarrating

    scraped_data.append(dict)


if __name__ == "__main__":
    
    print("threadstart", datetime.now().time())
    restaurant_URL_list = get_1000_restaurants()
    #print(restaurant_URL_list)

    with PoolExecutor(max_workers=4) as executor:
        for i in executor.map(try_threading, restaurant_URL_list):
            pass
        print("threadend", datetime.now().time())
        for j in executor.map(try_threading_each, test_yelp):
            pass

    dataFrame = pd.DataFrame.from_dict(scraped_data)
    dataFrame.to_csv('restaurant_data.csv',index = False)
    print("end", datetime.now().time())


