import pymysql
from db import DB
import pprint
from csv import reader
import pandas as pd

from dbtests import restaurant_data_tests 
from dbtests import reviews_data_tests 

from scraperhelpers import parse_thru_dishes
from scraperhelpers import parse_thru_foodtypes
from scraperhelpers import parse_thru_ratings
from scraperhelpers import parse_thru_reviews
from scraperhelpers import parse_thu_popular

def setup_db():
    '''Prompt user for MySql username and password then create a database instance

    '''
    
    global db
    
    try:
        db = DB()
    except:
        raise Exception("database parameters invalid. Check your user, pass, or the \"db\" field in db.py")


def open_csv_from_file(csv_file:str):
    with open(csv_file, "r") as read_obj:
        csv_reader = reader(read_obj)
    return csv_reader

def get_rid_from_name(restName:str):
    id_sql = "SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s"
    return (db.query(id_sql,restName)[0])['restaurant_id']
def get_menu_id(restName:str):
    menu_id_sql = "SELECT menu_id FROM menu WHERE restaurant_id = %s"
    return (db.query(menu_id_sql,restName)[0])['menu_id']

def insert_data(csv_file:str):
    rest_query = "INSERT INTO food_chat_db.restaurant(restaurant_name,city,star_rating,price_range,reservation,vegan_option,delivery_option,website) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    hours_query = "INSERT INTO food_chat_db.hoursAvailable(restaurant_id,monday_hours,tuesday_hours,wednesday_hours,thursday_hours,friday_hours,saturday_hours,sunday_hours) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    foodtype_query = "INSERT INTO food_chat_db.foodType(restaurant_id,food_type) VALUES (%s,%s)"
    review_query = "INSERT INTO food_chat_db.review(restaurant_id,review_content,rating) VALUES (%s,%s,%s)"
    dish_query= "INSERT INTO food_chat_db.dish(menu_id,dish_name,is_popular) VALUES (%s,%s,%s)"
    menu_query= "INSERT INTO food_chat_db.menu(restaurant_id) VALUES (%s)"

    df = pd.read_csv(csv_file)
    db.execute("USE food_chat_db")
    cleaned_df = df.replace({'Yes':True,'No':False,'Null': None })
    print(cleaned_df[['reservation','vegan_option','delivery_option']])
    for row in cleaned_df.itertuples(index=True,name='Pandas'):

        #print('Going to insert into the database now')
        
        db.execute(rest_query,tuple([getattr(row,"restaurant_name"),getattr(row,"city"),getattr(row,"star_rating"),getattr(row,"pricerange"),getattr(row,"reservation"),getattr(row,"vegan_option"),getattr(row,"delivery_option"),getattr(row,"restaurant_website")]))
        
        rest_id = get_rid_from_name(getattr(row,"restaurant_name"))
        
        rev_list = parse_thru_reviews(getattr(row,"reviews")) # list of review strings
        rate_list = parse_thru_ratings(getattr(row,"review_rating")) # list of review ratings
        foodtype_list = parse_thru_foodtypes(getattr(row,"cusine_types"))

        dish_list = parse_thru_dishes(getattr(row, "menu_dishes"))
        pop_list = parse_thu_popular(getattr(row,"popular_dishes"))
        
        for i in range(len(rev_list)):
           db.execute(review_query,tuple([rest_id,rev_list[i],rate_list[i]]))
        for i in foodtype_list:
            db.execute(foodtype_query,tuple([rest_id,i]))
        db.query(hours_query,tuple([rest_id,getattr(row,"monday_hours"),getattr(row,"tuesday_hours"),getattr(row,"wednesday_hours"),getattr(row,"thursday_hours"),getattr(row,"friday_hours"),getattr(row,"saturday_hours"),getattr(row,"sunday_hours")]))
        
        db.query(menu_query,tuple([rest_id]))#menu query

        menu_id = get_menu_id(rest_id) # finds menu_id through menu table from specific restaurant
        #print(dish_list)
        #print(len(dish_list))
        """ if len(dish_list) != 0: #check to ensure that the dishes were actually scraped
            for i in range(len(dish_list)):
                print(tuple([menu_id,dish_list[i],pop_list[i]]))
                #db.query(dish_query,tuple([menu_id,dish_list[i],pop_list[i]]))
        else:
            db.query(dish_query,tuple([menu_id,None,None])) """
        db.commit()
if __name__ == "__main__":
    setup_db()
    sql_commands = get_sql_commands_from_file('sql/create_all_tables.sql')
    drop_sql_cmmds = get_sql_commands_from_file('sql/drop_all_tables.sql')
    #delete tables if they exist
    for i in drop_sql_cmmds:
        #db.execute(i)
        print(i)

    #create tables if they don't exist
    for i in sql_commands:
        print('sql cmmd here')
        #db.execute(i)
        
    #next, open the csv file and insert the data

    csv_file = 'restaurant_data.csv'
    insert_data(csv_file)

    # now that the data exists, run tests to check health of tables/db
    db.execute("USE food_chat_db")
    #restaurant_data_tests(db)
    #print(db.query("SELECT review_content FROM food_Chat_db.review"))
    #reviews_data_tests(db)
    food_search = get_sql_commands_from_file('SQL/foodtypesearch.sql')

    #the following is an example SQL search
    for i in food_search:
        print(db.query(i,('Italian')))
    
   




            
        

