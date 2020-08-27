from config import Config
import pymysql
import pandas as pd

config = Config()
conn = pymysql.connect(host=config.MYSQL_DATABASE_HOST,
                       user=config.MYSQL_DATABASE_USER,
                       password='',
                       db=config.MYSQL_DATABASE_DB,
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

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


def upsert_restaurant_table(params: tuple):
    '''Given a tuple containing restaurant params, upsert

    '''

    rest_insert = get_sql_commands_from_file('SQL/upsert_restaurant.sql')[0]

    cursor.execute(rest_insert, tuple([getattr(params, 'restaurant_name'),
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
        cursor.execute(review_insert, (rest_id, review_list[i], rating_list[i]))


def upsert_food_type_table(food_type_list: list, rest_id: int):
    '''Upsert food type table given a list of food types

    '''
    foodtype_insert = get_sql_commands_from_file('SQL/upsert_food_type.sql')[0]

    for i in food_type_list:
        cursor.execute(foodtype_insert, tuple([rest_id, i]))


def upsert_hours_table(params: tuple, rest_id: int):
    '''Upsert food type table given a list of food types

    '''
    hours_upsert = get_sql_commands_from_file('SQL/upsert_hours.sql')[0]

    cursor.execute(hours_upsert, tuple([rest_id,
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
    cursor.execute(menu_insert, (rest_id))


def upsert_dish_table(dish_list: list, pop_dishes: list, rest_id: int):
    '''TODO: Look at why in menu table, there are multiple menus to a restaurant???
        TODO: why tf is pop_dishes and dish_list length not the same??
    '''

    cursor.execute(
        'SELECT menu_id FROM food_chat_db.menu WHERE restaurant_id = %s', rest_id)
    menu_id = cursor.fetchall()[0]['menu_id']
    dish_insert = get_sql_commands_from_file('SQL/upsert_dish.sql')[0]

    if len(dish_list) > 0:
        for i in range(len(dish_list)):
            dish_name = dish_list[i]
            if i > len(pop_dishes) - 1:
                is_popular = False
            else:
                is_popular = pop_dishes[i]
            cursor.execute(dish_insert, (dish_name, menu_id, is_popular))


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

    

def upsert_data(csv_file='data/restaurant_data.csv'):
    print('inserting data')
    

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
        cursor.execute('SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s',
                           getattr(row, 'restaurant_name'))
        rest_id = cursor.fetchall()[0]['restaurant_id']
        upsert_review_table(rest_id, review_list, rating_list)
        upsert_food_type_table(foodtype_list, rest_id)
        upsert_hours_table(row, rest_id)
        upsert_menu_table(rest_id)
        upsert_dish_table(dish_list, pop_dishes, rest_id)
    conn.commit()
    return rows

if __name__ == '__main__':
    upsert_data()