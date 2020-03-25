from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re

# for link in soup.select('span span a'):
#     print(link.string)

#PSEUDOCODE
#get all links to yelp 
#go inside each link
#inside each link, gather information
#...for link in list:..
#get information needed
#append to dictionary


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
        reserve = newsoup.select('div > div > div:nth-child(3) > div > div:nth-child(2) > span')[1].text
        reserve = reserve.strip()
        if re.match('^Yes|No|$', reserve) or re.match('^Yes|No|$',reserve):
            reservation = reserve

    except:
        reservation = "None"
    
    #get credit card info
    try:
        credit = newsoup.select('div > div:nth-child(2) > span:nth-child(2)')[0].text
        credit = credit.strip()
        if re.match('^Yes|No|$', credit) or re.match('^Yes|No|$',credit):
            creditcard = credit

    except:
        creditcard = "None"

    #get takeout information 
   
    #get website of restaurant
    try:
        restwebsite = newsoup.select('div > div > p:nth-child(2) > a')[0].text
    except:
        restwebsite = "None"

    #add data to the dictionary
    dict['restaurant_name'] = name
    dict['city'] = city
    dict['starrating'] = starrating
    dict['pricerange'] = pricerange
    dict['reservation'] = reservation
    dict['creditcard'] = creditcard
    #dict['takeout'] = takeout
    dict['restaurant website'] = restwebsite   

    #append the scraped data to the list
    scraped_data.append(dict)

dataFrame = pd.DataFrame.from_dict(scraped_data)
dataFrame.to_csv('restaurant_data.csv',index = False)



