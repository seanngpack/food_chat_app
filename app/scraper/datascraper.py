from selenium import webdriver
import numpy
import requests
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#Reminder DB REQS: rest_name, rest_cuisine, city, stars, price range, Reservations, takesCredit,URL
# goal is to create a dictionary like:
"""
    {uniq_rest1:{name:non_uniq_name,stars:num_stars,cuisine_tags:[tag1,tag2,tag3],price_range:num_dollars},
    uniq_rest2:{name:non_uniq_name,stars:num_stars,cuisine_tags:[tag1,tag2],price_range:num_dollars},
    uniq_rest3:{name:non_uniq_name,stars:num_stars,cuisine_tags:[tag1],price_range:num_dollars}
    }
"""
def create_db_dictionary():
    #first open up yelp and search for restaurants
    driver = webdriver.Chrome() 
    driver.get('https://www.yelp.com/')
    time.sleep(5) # Let the user actually see something!
    search_box = driver.find_element_by_xpath('//*[@id="header_find_form"]/div/div[1]/div/label')
    search_box.send_keys('Restaurants')
    search_box.submit()
    
    #from results obtain a list of restaurant links
    time.sleep(5)
    main_list = '//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li'
    items=driver.find_elements_by_xpath(main_list) # will find a list of web objects that belong to /ul

    rest_url_list=[] #initiate empty restaurant list
    for item_id in range(0,len(items)): # TO DO- use try and catch to ensure there are no errors when adding to list
        if item_id >= 6: #this will ensure that the list will go below the sponsored restaurants
            rest=driver.find_element_by_xpath(main_list+'['+ str(item_id) +']'+'/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a')
            url= rest.get_attribute('href')
            rest_url_list.append(url)
    
    #once we have the list loop through the list to open new pages and get more info
    
    # QUESTION: should we connect to the DB here and get unique ids from the DB?? 
    db_dict={}
    uniq_counter=0
    for rests in rest_url_list:
        cuisine_list=[]
        uniq_counter+=1
        rest_dict={}
        driver.get(rests) #opens new page
        time.sleep(5)
        name=driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/h1').text
        rest_dict['name']=name #get the name of rest
        # TO DO fill rest in
        rest_dict['stars']=0 # get stars
        rest_dict['cuisine_tags']=cuisine_list
        rest_dict['price_range']=0
        rest_dict['city_name']=''
        rest_dict['takes_reservations']=0,
        rest_dict['takes_credit']=0,
        rest_dict['rest_url']=driver.current_url
        db_dict[uniq_counter]=rest_dict #ideally would like to create a unique id for each restaurant object added to the list
    print(db_dict)
    time.sleep(5)
    driver.quit()

create_db_dictionary()
#IGNORE BELOW FOR NOW
""" 
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.yelp.com/')
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_xpath('//*[@id="header_find_form"]/div/div[1]/div/label')
search_box.send_keys('Restaurants')
search_box.submit()

time.sleep(10)
main_list = '//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li'
#entire uL 
#ignore this main_list = '//*[@id="search-results"]/div[2]/ol'
actual_url = '//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li[2]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a'
items=driver.find_elements_by_xpath(main_list)
#li_items=items.find_elements_by_xpath('/li')
actual_part2= '//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li[6]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a'
#restaurant=driver.find_element_by_xpath(actual_part2)
#print(restaurant.get_attribute('href'))
rest_url_list=[]
for item_id in range(0,len(items)):
    if item_id >= 6:
        rest=driver.find_element_by_xpath(main_list+'['+ str(item_id) +']'+'/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a')
        url= rest.get_attribute('href')
        rest_url_list.append(url)

# this is the xpath that contains pretty much the entire page
main_restaurant_page= '//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]'
#left side of the page
main_left_page= '//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]'
#right side of the page
main_right_page= '//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[2]'
#general name info block containing name,stars,cuisine,money
gen_name_info='//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div'
# rest_name='//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/h1'
# //*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/h1
num_dollar_signs='//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/span[1]/span'
#multiple tags for cuisines, must use xpath as a list to find individual xpaths
cuisine_tags='//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/span[2]'
#num of stars given by the 'aria-label' value which lists a STRING that must be decoded
num_stars='//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/span/div'


rest_name_list=[]
for rests in rest_url_list:
    driver.get(rests)
    time.sleep(5)
    print('about to start a name search')
    name=driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[1]/h1').text
    rest_name_list.append(name) 

# xpath of first element
#first_elem = '//*[@id="search-results"]/div[2]/ol/li[1]'
# now need to search under All Results
#all_results = '//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/ul/li[5]' #xpath of all results
#entire oL 
#main_list = '//*[@id="search-results"]/div[2]/ol' """





