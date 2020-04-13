from food_chat_app.models.db.db import DB
from flask import current_app as app
import pandas as pd

'''Contains commands you can run to the database
'''

db = DB()


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


def upsert_data(csv_file='data/restaurant_data.csv'):
    '''Inserts data from csv file to the database.
    I guess this basically assumes there's a clean database.

    Args:
        csv_file (str): the path to the csv file.

    Returns:
        Number of rows updated/inserted

    '''

    df = pd.read_csv(csv_file)
    cleaned_df = df.replace({'Yes': True, 'No': False, 'Null': None})
    rows = cleaned_df.shape[0]
    # print(cleaned_df[['reservation', 'vegan_option', 'delivery_option']])
    for row in cleaned_df.itertuples(index=True, name='Pandas'):
        review_list = getattr(row, 'reviews').replace('¬†', '').split('>')
        rating_list = getattr(row, 'review_rating').split(', ')
        foodtype_list = getattr(row, 'cusine_types').split(', ')
        if getattr(row, 'menu_dishes') is not None:
            dish_list = getattr(row, 'menu_dishes').split(', ')
        else:
            dish_list = []
        pop_dishes = _parse_popular(getattr(row, 'popular_dishes'))

        upsert_restaurant_table(row)
        rest_id = db.query('SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s',
                           getattr(row, 'restaurant_name'))[0]['restaurant_id']
        upsert_review_table(rest_id, review_list, rating_list)
        upsert_food_type_table(foodtype_list, rest_id)
        upsert_hours_table(row, rest_id)
        upsert_menu_table(rest_id)
        upsert_dish_table(dish_list, pop_dishes, rest_id)
    db.commit()
    return rows


def upsert_restaurant_table(params: tuple):
    '''Given a tuple containing restaurant params, upsert

    '''

    rest_insert = get_sql_commands_from_file('SQL/upsert_restaurant.sql')[0]

    db.execute(rest_insert, tuple([getattr(params, 'restaurant_name'),
                                   getattr(params, 'city'),
                                   getattr(params, 'star_rating'),
                                   getattr(params, 'pricerange'),
                                   getattr(params, 'reservation'),
                                   getattr(params, 'vegan_option'),
                                   getattr(params, 'delivery_option'),
                                   getattr(params, 'restaurant_website')]))


def upsert_review_table(rest_id: int, review_list: list, rating_list: list):
    '''upsert review table given parameters

    '''

    review_insert = get_sql_commands_from_file('SQL/upsert_reviews.sql')[0]
    # insert the reviews
    for i in range(len(review_list)):
        db.execute(review_insert, (rest_id, review_list[i], rating_list[i]))


def upsert_food_type_table(food_type_list: list, rest_id: int):
    '''Upsert food type table given a list of food types

    '''
    foodtype_insert = get_sql_commands_from_file('SQL/upsert_food_type.sql')[0]

    for i in food_type_list:
        db.execute(foodtype_insert, tuple([rest_id, i]))


def upsert_hours_table(params: tuple, rest_id: int):
    '''Upsert food type table given a list of food types

    '''
    hours_upsert = get_sql_commands_from_file('SQL/upsert_hours.sql')[0]

    db.execute(hours_upsert, tuple([rest_id,
                                    getattr(params, 'monday_hours'),
                                    getattr(params, 'tuesday_hours'),
                                    getattr(params, 'wednesday_hours'),
                                    getattr(params, 'thursday_hours'),
                                    getattr(params, 'friday_hours'),
                                    getattr(params, 'saturday_hours'),
                                    getattr(params, 'sunday_hours')]))


def upsert_menu_table(rest_id: int):
    '''Upsert menu table given a restaurant id

    '''

    menu_insert = get_sql_commands_from_file('SQL/upsert_menu.sql')[0]
    db.execute(menu_insert, (rest_id))


def upsert_dish_table(dish_list: list, pop_dishes: list, rest_id: int):
    '''TODO: Look at why in menu table, there are multiple menus to a restaurant???
        TODO: why tf is pop_dishes and dish_list length not the same??
    '''

    menu_id = db.query(
        'SELECT menu_id FROM food_chat_db.menu WHERE restaurant_id = %s', rest_id)[0]['menu_id']
    dish_insert = get_sql_commands_from_file('SQL/upsert_dish.sql')[0]

    if len(dish_list) > 0:
        for i in range(len(dish_list)):
            dish_name = dish_list[i]
            if i > len(pop_dishes) - 1:
                is_popular = False
            else:
                is_popular = pop_dishes[i]
            db.execute(dish_insert, (dish_name, menu_id, is_popular))


def _parse_popular(pop_list: str):
    ''' helper function that returns a list of popular or not dishes'''
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


def proximity_query(entity: str):
    '''Find restaurants given a city or location.

    Args:
        location

    Returns:
        a list of restaurants or None if no results

    '''

    proximity_query = db.query(get_sql_commands_from_file(
        'SQL/proximity_search.sql')[0], (entity, ))

    if type(proximity_query) is not list:
        return None
    else:
        return proximity_query


def random_query():
    '''

    '''

    random_search = db.query(
        get_sql_commands_from_file('SQL/random_search.sql')[0])
    if type(random_search) is not list:
        return None
    else:
        return random_search


def food_type_query(entity: str):
    ''' Finds restaurants based on cuisine type

    Args:
        food type hopefully

    '''

    food_type_query = db.query(get_sql_commands_from_file(
        'SQL/food_type_search.sql')[0], (entity, ))
    if type(food_type_query) is not list:
        return None
    else:
        return food_type_query


def name_search_query(entity: str):
    ''' Finds restaurant id that matches the given name '''
    name_search_query = db.query(get_sql_commands_from_file(
        'SQL/name_search.sql')[0], (entity, ))
    if type(name_search_query) is not list:
        return None
    else:
        return name_search_query


def rest_props_query(entity: str):
    ''' Finds restaurant details  that matches the given id '''
    rest_props_query = db.query(get_sql_commands_from_file(
        'SQL/rest_details.sql')[0], (entity, ))
    if type(rest_props_query) is not list:
        return None
    else:
        return rest_props_query


def hours_props_query(entity: str):
    ''' Finds restaurant hours that matches the given id '''
    hours_props_query = db.query(get_sql_commands_from_file(
        'SQL/hours_detail.sql')[0], (entity, ))
    if type(hours_props_query) is not list:
        return None
    else:
        return hours_props_query


def review_props_query(entity: str):
    ''' Finds restaurant query review info that matches the given id '''
    review_props_query = db.query(get_sql_commands_from_file(
        'SQL/reviews_details.sql')[0], (entity, ))
    if type(review_props_query) is not list:
        return None
    else:
        return review_props_query


def rating_query(entity: str):
    '''Find rating given a restaurant.

    Args:
        restaurant name

    Returns:
        a list of rating for a restaurant or None if no results

    '''
    rating_query = db.query(get_sql_commands_from_file(
        'SQL/rating_search.sql')[0], (entity, ))

    if type(rating_query) is not list:
        return None
    else:
        return rating_query


def vegan_query(entity: str):
    '''Find a list of vegan restaurants

    Args:
        Don't really need args for this one

    Returns:
        a list of restaurants or None if no results

    '''

    vegan_query = db.query(get_sql_commands_from_file(
        'SQL/vegan_search.sql')[0])

    if type(vegan_query) is not list:
        return None
    else:
        return vegan_query


def insert_user(user_id: str):
    ''' insert the user to the user table. If exists, then do nothing

    '''

    user_insert = get_sql_commands_from_file('SQL/insert_user.sql')[0]
    db.execute(user_insert, (user_id,))


def insert_message(user_id: str, message: str):
    '''Store the user message given a user_id and message

    '''

    message_insert = get_sql_commands_from_file('SQL/insert_message.sql')[0]
    db.execute(message_insert, (user_id, message,))
