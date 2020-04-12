import abc
import food_chat_app.models.db.commands as db_commands
import random
import csv
from csv import reader

class IntentStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, entity):
        pass


class ProximityStrategy(IntentStrategy):
    def __init__(self):
        self.foodly_db = DB()
    def execute(self, entity):
        self.foodly_db.execute("USE food_chat_db")
        proximity_query = self.foodly_db.query(import_sql_from_file('SQL/proximitysearch.sql'),entity)
        if len(proximity_query) != 0:
            proximity_list=[elem['restaurant_name'] for elem in proximity_query]
            shuffle_list = random.sample(proximity_list,len(proximity_list))
            prompt = 'Here are some restaurants to checkout in '+entity+': '
            #print(shuffle_list)
            if len(shuffle_list)>10:
                results = ','.join(shuffle_list[0:10])
            else:
                results = ','.join(shuffle_list)
            proximityresponse = (prompt+results)
        else:
            proximityresponse = "Sorry, no restaurants found in: "+entity+". Please try searching again."
        print(proximityresponse)
        return(proximityresponse)


class FoodTypeStrategy(IntentStrategy):
    def execute(self, entity):
        print('food type search' + entity)
        return 'food type search ' + entity


class RatingStrategy(IntentStrategy):
    def execute(self, entity):
        print('rating search' + entity)
        return 'rating search ' + entity


class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name search' + entity)
        return 'name search ' + entity


class RandomStrategy(IntentStrategy):
    def __init__(self):
        self.foodly_db = DB()
    def execute(self, entity):
        self.foodly_db.execute("USE food_chat_db")
        csvfile = open("test_rest_data.csv")
        reader = csv.reader(csvfile)
        lines= len(list(reader))
        randomID = random.randint(1,lines)
        random_query = self.foodly_db.query(import_sql_from_file('SQL/randomsearch_byid.sql'),str(randomID))
        if len(random_query)!=0:
            for elem in random_query:
                random_name = elem['restaurant_name']
                random_city = elem['city']
                random_starrating = elem['star_rating']
                random_pricerange = elem['price_range']
                random_res = elem['reservation']
                random_veg = elem['vegan_option']
                random_deliv = elem['delivery_option']
                random_web = elem['website']
            prompt = """Would you like to try this restaurant: %s, 
                        located in: %s, 
                        star rating: %s, 
                        price_range: %s, 
                        offers reservation: %s, 
                        offers vegan option: %s, 
                        offers delivery: %s, 
                        website: %s"""
            print(prompt % (random_name,random_city, random_starrating, random_pricerange, 
            random_res, random_veg, random_deliv, random_web))
        else:
            RandomStrategy.execute(self,entity)
        
        responseprompt = (prompt % (random_name,random_city, random_starrating, random_pricerange, 
            random_res, random_veg, random_deliv, random_web))
        print(responseprompt)
        return responseprompt

class NullStrategy(IntentStrategy):
    def execute(self, entity):
        print('null search' + entity)
        return 'null search ' + entity


class GratitudeStrategy(IntentStrategy):
    def execute(self, entity):
        print('gratitude' + entity)
        return 'gratitude ' + entity
