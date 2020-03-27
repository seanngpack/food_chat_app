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
    menu_dict = {}

    newpage = requests.get(yelp_url, timeout = 15)
    newsoup = BeautifulSoup(newpage.content, 'html.parser')  
    
    #get name of restaurant
    try:
        name = newsoup.select('div > div > div:nth-child(1) > h1')[0].text
    except:
        name = "None"

    menu_dict['restaurant_name'] = name

    scraped_data.append(menu_dict)

dataFrame = pd.DataFrame.from_dict(scraped_data)
dataFrame.to_csv('menu_data.csv',index = False)
