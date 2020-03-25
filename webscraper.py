from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re

#create a list to store the scraped data
scraped_data = []

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

#looping through each restaurant url from list
for yelp_url in yelp_link:

    #initialize dictionary
    dict = {}

    newpage = requests.get(yelp_url, timeout = 15)
    newsoup = BeautifulSoup(newpage.content, 'html.parser')  
    
    #get name of restaurant
    try:
        name = newsoup.select('div > div > div:nth-child(1) > h1')[0].text
    except:
        name = "None"

    #get city
    try: 
        cityname = newsoup.select('address > p:nth-child(2) > span')[0].text
        cityname = cityname.split(',')
        cityname = cityname[0]
        if re.match("^\S+$", cityname):
            city = cityname
    except:
        city = "None"

    #get star rating 
    try:
        stars= newsoup.find(class_ = re.compile("i-star"))['aria-label']
        stars = str(stars)
        stars = stars.split(' ')
        starrating = stars[0]
    except:
        starrating = "None"

    #get dollar signs
    try:
        price = newsoup.select('div > div > span:nth-child(3) > span')[0].text
        if re.match("^\$", str(price)):
            pricerange = price
    except:
        pricerange = "None"

    #get reservation info
    try:
        #for i in range(0,12):
        reserve = newsoup.find_all('#expander-link-content-b6bc3146-0a7c-48e2-9011-3676ef9ba8da > div > div>div>div')[1].text
        print(reserve)
        # reserve = reserve.strip()
        # if re.match('^Yes|No|$', reserve) or re.match('^Yes|No|$',reserve):
        #     reservation = reserve

    except:
        reservation = "None"
    
    #get credit card info
    try:
        credit = newsoup.select('div > div > div:nth-child(6) > div > div:nth-child > span')[2].text
        print(credit)
        # credit = credit.strip()
        # if re.match('^Yes|No|$', credit) or re.match('^Yes|No|$',credit):
        #     creditcard = credit

    except:
        creditcard = "None"

    #get takeout information
    try:
        take = newsoup.select('div > div > div:nth-child(5) > div > div:nth-child(2) > span')[1].text
        take = take.strip()
        if re.match('^Yes|No|$', take) or re.match('^Yes|No|$',take):
            takeout = take

    except:
        takeout = "None"
   
    #get website of restaurant
    try:
        restwebsite = newsoup.select('div > div > p:nth-child(2) > a')[0].text
    except:
        restwebsite = "None"


    #get monday hours
    try:
        mondayhours = newsoup.select('tbody > tr:nth-child(1)>td:nth-child(2)')[0].text
    except:
        mondayhours = "None"
    
    #get tuesday hours
    try:
        tuesdayhours = newsoup.select('tbody > tr:nth-child(2)>td:nth-child(2)')[0].text
    except:
        tuesdayhours = "None"
    

    #get wednesday hours
    try:
        wednesdayhours = newsoup.select('tbody > tr:nth-child(3)>td:nth-child(2)')[0].text
    except:
        wednesdayhours = "None"
    
    #get thursday hours
    try:
        thursdayhours = newsoup.select('tbody > tr:nth-child(4)>td:nth-child(2)')[0].text
    except:
        thursdayhours = "None"

    #get friday hours
    try:
        fridayhours = newsoup.select('tbody > tr:nth-child(5)>td:nth-child(2)')[0].text
    except:
        fridayhours = "None"
    

    #get wednesday hours
    try:
        saturdayhours = newsoup.select('tbody > tr:nth-child(6)>td:nth-child(2)')[0].text
    except:
        saturdayhours = "None"
    
    #get thursday hours
    try:
        sundayhours = newsoup.select('tbody > tr:nth-child(7)>td:nth-child(2)')[0].text
    except:
        sundayhours = "None"

    #add data to the dictionary
    dict['restaurant_name'] = name
    dict['city'] = city
    dict['star_rating'] = starrating
    dict['pricerange'] = pricerange
    #dict['reservation'] = reservation
    dict['credit_card'] = creditcard
    dict['takeout'] = takeout
    dict['restaurant_website'] = restwebsite   
    dict['monday_hours'] = mondayhours
    dict['tuesday_hours'] = tuesdayhours
    dict['wednesday_hours']=wednesdayhours
    dict['thursday_hours'] = thursdayhours
    dict['friday_hours'] = fridayhours
    dict['saturday_hours'] = saturdayhours
    dict['sunday_hours'] = sundayhours

    #append the scraped data to the list
    scraped_data.append(dict)



dataFrame = pd.DataFrame.from_dict(scraped_data)
dataFrame.to_csv('restaurant_data.csv',index = False)



