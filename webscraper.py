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

#global variables
#create a list to store the scraped data
scraped_data = []
newsoup = None
yelp_link = []
  
# code snippet whose execution time is to be measured 

def check_if_popular(pop_list, menu_list):
    popular =[]
    for menu_item in menu_list:
        if menu_item in pop_list:
            popular.append("yes")
        else:
            popular.append("no")

    pop = ', '.join(map(str,popular))
    return pop


def get_restaurant_yelp_link():
    global yelp_link
    print("yelp link start",datetime.now().time())
    for i in range(0,60,30):
        URL = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Boston%2C%20MA&start="+str(i)
        #page = requests.get(URL, stream = True, timeout = 3)
        page = urllib.request.urlopen(URL)
        soup = BeautifulSoup(page, 'lxml')   
        #find all the links to yelp page
        #gets link for each restaurant in the list  
        #for link in soup.select('h4 span a'):
        print("startyelplist" ,datetime.now().time())
        for link in soup.find_all('a', class_ = 'lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'):
            #filters out the ads
            print("start filter",datetime.now().time() )
            if re.match('^/biz',str(link['href'])):
                yelp_link.append("https://yelp.com"+str(link['href']))
        print("endyelplist" ,datetime.now().time())
    print("yelp link end",datetime.now().time())  

def create_dict():
    global scraped_data
    global newsoup
    #looping through each restaurant url from list
    for yelp_url in yelp_link:
        #initialize dictionary
        dict = {}
        print("inner yelp link start",datetime.now().time())
        newpage = requests.get(yelp_url, stream = True, timeout = 5)
        print("request done", datetime.now().time())
        newsoup = BeautifulSoup(newpage.text, 'lxml') 
        print("beautifulsoup",datetime.now().time() )

        print("restaurant name start",datetime.now().time())
        #get name of restaurant
        try:
            #name = newsoup.select('div > div > div:nth-child(1) > h1')[0].text
            name = newsoup.find('h1', class_ = 'lemon--h1__373c0__2ZHSL heading--h1__373c0__1VUMO heading--no-spacing__373c0__1PzQP heading--inline__373c0__1F-Z6').text
        except:
            name = "Null"
        print("restaurant name end",datetime.now().time())

        #get city
        print("restaurant city start",datetime.now().time())
        try: 
            cityname = newsoup.select_one('address > p:nth-child(2) > span').text.split(',')[0]
            if re.match("^\S+$", cityname):
                city = cityname
        except:
            city = "Null"
        print("restaurant city end",datetime.now().time())


        #get star rating 
        print("restaurant star start",datetime.now().time())
        try:
            starrating= newsoup.find(class_ = re.compile("i-stars--large"))['aria-label'].split(' ')[0]
            #starrating = (str(stars)).split(' ')[0]
        except:
            starrating = "Null"
        print("restaurant star end",datetime.now().time())

        #get dollar signs
        print("restaurant dollar start",datetime.now().time())
        try:
            #price = newsoup.select('div > div > span:nth-child(3) > span')[0].text
            price =  newsoup.find('span', class_='lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-bullet--after__373c0__1ZHaA text-size--large__373c0__1568g').text
            if re.match("^\$", str(price)):
                pricerange = price
        except:
            pricerange = "Null"
        print("restaurant dollar end",datetime.now().time())

        #get reservation info
        print("restaurant reserve start",datetime.now().time())
        try:
            r = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            print("restaurant reserve end",datetime.now().time())
            print("restaurant reserve strip start",datetime.now().time())
            for m in r:
                amenities = m.text
                if re.findall("Takes Reservation",str(amenities)):
                    reserve = amenities.split('\xa0')[-1]
                    if re.match('^Yes|No|$', reserve) or re.match('^Yes|No|$',reserve):
                        reservation = reserve
            print("restaurant reserve strip end",datetime.now().time())

        except:
            reservation = "Null"
        print("restaurant reserve end",datetime.now().time())

        #get vegan option info
        print("restaurant vegan start",datetime.now().time())
        try:
            #v = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            for m in r:
                amenities = m.text
                if re.findall("Vegan Option",str(amenities)):
                    veg = amenities.split('\xa0')[-1]
                    if re.match('^Yes|No|$', veg) or re.match('^Yes|No|$', veg):
                        vegan = veg

        except:     
            vegan = "Null"
        print("restaurant vegan end",datetime.now().time())

        #get delivery information
        print("restaurant delivery start",datetime.now().time())
        try:
            #d = newsoup.find_all('div', class_ = re.compile("lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"))
            for m in r:
                amenities = m.text
                if re.findall("Offers Delivery",str(amenities)):
                    deliv = amenities.split('\xa0')[-1]
                    if re.match('^Yes|No|$', deliv) or re.match('^Yes|No|$', deliv):
                        delivery= deliv

        except:
            delivery = "Null"

        print("restaurant delivery end",datetime.now().time())

        #get website of restaurant
        print("restaurant website start",datetime.now().time())
        try:
            restwebsite = newsoup.select('div > div > p:nth-child(2) > a')[0].text
        except:
            restwebsite = "Null"
        print("restaurant website end",datetime.now().time())

        #get cusine type of restaurant 
        print("restaurant cusine start",datetime.now().time())
        try:
            c = []
            ctype = newsoup.select("div > div > span > span > a")
            c =[a.text for a in ctype]
            cusinetype = ', '.join(map(str,c))
                
        except:
            cusinetype = "Null"
        print("restaurant cusine end",datetime.now().time())

        #get monday hours
        print("restaurant hours start",datetime.now().time())
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
        

        #get wednesday hours
        try:
            saturdayhours = newsoup.select_one('tbody > tr:nth-child(6)>td:nth-child(2)').text
        except:
            saturdayhours = "Null"
        
        #get thursday hours
        try:
            sundayhours = newsoup.select_one('tbody > tr:nth-child(7)>td:nth-child(2)').text
        except:
            sundayhours = "Null"
        print("restaurant hours end",datetime.now().time())

        #get popular dishes
        print("all dishes start",datetime.now().time())
        try:
            dish_list = []
            popular_list =[]

            #looks for popular dishes
            print("popular dish list start",datetime.now().time())
            #p = newsoup.find_all('p', class_ = re.compile("lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text--truncated__373c0__3IHqb"))
            #appends to popular dish list 
            #popular_list=[dish.text for dish in]
            popular_list = [dish.text for dish in newsoup.find_all('p', class_ = re.compile("lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text--truncated__373c0__3IHqb"))]
            print("popular dish list end",datetime.now().time())
            
            print("menu link start",datetime.now().time())
            #looks for restaurant menu
            m = newsoup.select_one("div > div:nth-child(4) > div > div.lemon--div__373c0__1mboc.arrange-unit__373c0__1piwO.arrange-unit-fill__373c0__17z0h.border-color--default__373c0__2oFDT > p > a")
            menuURL = "https://yelp.com"+ m['href']
            menupage = requests.get(menuURL,timeout=1)
            menusoup = BeautifulSoup(menupage.text, 'lxml')
            print("menu link end",datetime.now().time())


            #appends to menu list
            print("search menu dish start",datetime.now().time())
            dish = menusoup.find_all("h4")
            dish_list=[d.text.strip()for d in dish]
            print("search menu dish end",datetime.now().time())

            print("menu dish get start",datetime.now().time())
            #gets all the dishes on the menu
            menudish = ', '.join(map(str,dish_list))
            #print(menudish)
            dishes = menudish
            print("menu dish get end",datetime.now().time())

            print("search pop dish start",datetime.now().time())
            #check if dish is popular

            popular = check_if_popular(popular_list, dish_list)
            print("search pop dish end",datetime.now().time())
        
        except:
            dishes = "Null"
            popular = "Null"
        print("all dishes end",datetime.now().time())

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

        print("add data to dictionary start",datetime.now().time())
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
        print("add data to dictionary end",datetime.now().time())

        print("scraped data append start",datetime.now().time())
        #append the scraped data to the list
        scraped_data.append(dict)
        print("scraped data append start",datetime.now().time())

    print("inner yelp link end",datetime.now().time())
    print("done one restaurant")

if __name__ == "__main__":
    restaurant_yelp_link = get_restaurant_yelp_link()

    create_dict()

    dataFrame = pd.DataFrame.from_dict(scraped_data)
    dataFrame.to_csv('restaurant_data.csv',index = False)



