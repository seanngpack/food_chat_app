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
    def execute(self, entity):
        if entity is None:
            return 'please type your question again'

        proximity_query = db_commands.proximity_query(entity)
        if len(proximity_query) != 0:
            proximity_list = [elem['restaurant_name']
                              for elem in proximity_query]
            shuffle_list = random.sample(proximity_list, len(proximity_list))
            prompt = 'Here are some restaurants to checkout in '+entity+': '
            # print(shuffle_list)
            if len(shuffle_list) > 10:
                results = ','.join(shuffle_list[0:10])
            else:
                results = ','.join(shuffle_list)
            proximityresponse = (prompt+results)
        else:
            proximityresponse = "Sorry, no restaurants found in: " + \
                entity+". Please try searching again."

        return proximityresponse


class FoodTypeStrategy(IntentStrategy):
    def execute(self, entity):
        if entity == 'Vegan' or entity == 'vegan':
            vegan_query = db_commands.vegan_query(entity)
            if type(vegan_query) == list:
                rest_list=[]
                for elem in vegan_query:
                    rest_list.append(elem['restaurant_name'])
                prompt = "Here are some places with vegan options to checkout:"
                results = ", ".join( str(e) for e in rest_list ) 
                
                return prompt,results
            else:
                return "What are you looking for with vegan? Please try searching again."     
        elif entity != 'Vegan' or entity != 'vegan':
            foodtype_query = db_commands.food_type_query(import_sql_from_file("SQL/foodtypesearch.sql"),entity)
            if type(foodtype_query) == list:
                rest_list=[]
                for elem in foodtype_query:
                    rest_list.append(elem['restaurant_name'])
                prompt = "Here are some restaurants to checkout:"
                results = ", ".join( str(e) for e in rest_list ) 
                
                return prompt,results
            else:
                return "Couldn't find what you were looking for, please try again!" 
        else:
            return "Sorry, couldn't find that. Please try asking something else."


class RatingStrategy(IntentStrategy):
    def execute(self, entity):
        print('rating search' + entity)
        return 'rating search ' + entity


class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name search' + entity)
        return 'name search ' + entity


class RandomStrategy(IntentStrategy):
    def execute(self, entity):
        
        random_query = db_commands.random_query()
        if len(random_query) != 0:
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
            print(prompt % (random_name, random_city, random_starrating, random_pricerange,
                            random_res, random_veg, random_deliv, random_web))
        else:
            RandomStrategy.execute(self, entity)

        responseprompt = (prompt % (random_name, random_city, random_starrating, random_pricerange,
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
