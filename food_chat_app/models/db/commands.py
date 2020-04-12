from food_chat_app.models.db.db import DB
from flask import current_app as app


'''Contains commands you can run to the database
'''

db = DB()
try:
    db.execute(f'USE {app.config["DB_NAME"]}')
except:
    print('ERROR: flask server not loaded or database doesn\'t exist')


def get_sql_commands_from_file(sql_file: str):
    '''Given a file, loads the sql statements delineated by ;

    Args:
        sql_file (str): the file path of the file

    Returns:
        a list of the sql commands in the file

    '''

    with open(sql_file) as file:
        text = file.read()
        sql_commands = [x.replace('\n', '') for x in text.split(';') if x]
        return sql_commands


def drop_all_tables():
    sql_commands = get_sql_commands_from_file('sql/drop_all_tables.sql')
    for cmd in sql_commands:
        db.execute(cmd)


def insert_data(csv_file: str):
    import pandas as pd
    '''Inserts data from csv file to the database.
    I guess this basically assumes there's a clean database.

    Args:
        csv_file (str): the path to the csv file.

    '''
    rest_insert = 'INSERT INTO food_chat_db.restaurant(restaurant_name,city,star_rating,price_range,reservation,vegan_option,delivery_option,website) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    hours_insert = 'INSERT INTO food_chat_db.hoursAvailable(restaurant_id,monday_hours,tuesday_hours,wednesday_hours,thursday_hours,friday_hours,saturday_hours,sunday_hours) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    foodtype_insert = 'INSERT INTO food_chat_db.foodType(restaurant_id,food_type) VALUES (%s,%s)'
    review_insert = 'INSERT INTO food_chat_db.review(restaurant_id,review_content,rating) VALUES (%s,%s,%s)'
    # dish_query = 'INSERT INTO food_chat_db.dish(menu_id,dish_name,is_popular) VALUES (%s,%s,%s)'
    menu_insert = 'INSERT INTO food_chat_db.menu(restaurant_id) VALUES (%s)'

    df = pd.read_csv(csv_file)

    cleaned_df = df.replace({'Yes': True, 'No': False, 'Null': None})
    # print(cleaned_df[['reservation', 'vegan_option', 'delivery_option']])
    for row in cleaned_df.itertuples(index=True, name='Pandas'):
        db.execute(rest_insert, tuple([getattr(row, 'restaurant_name'),
                                       getattr(row, 'city'),
                                       getattr(row, 'star_rating'),
                                       getattr(row, 'pricerange'),
                                       getattr(row, 'reservation'),
                                       getattr(row, 'vegan_option'),
                                       getattr(row, 'delivery_option'),
                                       getattr(row, 'restaurant_website')]))

        rest_id = db.query('SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s',
                           getattr(row, 'restaurant_name'))[0]['restaurant_id']

        rev_list = getattr(row, 'reviews').replace('¬†', '').split('>')

        rating_list = getattr(row, 'review_rating').split(', ')

        foodtype_list = getattr(row, 'cusine_types').split(', ')

        if getattr(row, 'menu_dishes') is not None:
            dish_list = getattr(row, 'menu_dishes').split(', ')
        else:
            dish_list = []

        pop_list = parse_popular(getattr(row, 'popular_dishes'))

        # insert the reviews
        for i in range(len(rev_list)):
            db.execute(review_insert, tuple(
                [rest_id, rev_list[i], rating_list[i]]))

        # insert the foodtypes
        for i in foodtype_list:
            db.execute(foodtype_insert, tuple([rest_id, i]))
        db.execute(hours_insert, tuple([rest_id,
                                        getattr(row, 'monday_hours'),
                                        getattr(row, 'tuesday_hours'),
                                        getattr(row, 'wednesday_hours'),
                                        getattr(row, 'thursday_hours'),
                                        getattr(row, 'friday_hours'),
                                        getattr(row, 'saturday_hours'),
                                        getattr(row, 'sunday_hours')]))

        db.execute(menu_insert, tuple([rest_id]))
        db.commit()


def parse_popular(pop_list: str):
    """ helper function that returns a list of popular or not dishes"""
    if type(pop_list) != str:
        popularity = []
    else:
        popularity = pop_list.split(", ")
        #print('The actual popularity list is: ',popularity)
        #print('Popularity length is:',len(popularity))
        for index, item in enumerate(popularity):
            if item == 'yes':
                popularity[index] = True
            elif item == 'no':
                popularity[index] = False
            else:
                popularity[index] = None
    return popularity
