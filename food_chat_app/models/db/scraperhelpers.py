
def parse_thru_reviews(rev_list:str):
    """ helper function that returns a list of cleaned restaurant reviews
    """
    cleaned = rev_list.replace("¬†","")
    reviews = cleaned.split(">")
    return reviews

def parse_thru_ratings(rating_list:str):
    """ helper function that returns a list of ratings
    """
    ratings = rating_list.split(", ")
    return ratings

def parse_thru_foodtypes(type_list:str):
    """ helper function that returns a list of food types"""
    types = type_list.split(", ")
    return types

def parse_thru_dishes(dish_list:str):
    """ helper function returns a list of dishes at a specific restaurant"""
    if type(dish_list) != str:
        dishes = []
    else:
        dishes = dish_list.split(", ")
    return dishes

def parse_thu_popular(pop_list:str):
    """ helper function that returns a list of popular or not dishes"""
    if type(pop_list) != str:
        popularity = []
    else:
        popularity = pop_list.split(", ")
        #print('The actual popularity list is: ',popularity)
        #print('Popularity length is:',len(popularity))
        for index,item in enumerate(popularity):
            if item == 'yes':
                popularity[index] = True
            elif item == 'no':
                popularity[index] = False
            else:
                popularity[index] = None
    return popularity
