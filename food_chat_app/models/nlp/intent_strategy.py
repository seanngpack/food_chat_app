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
        if proximity_query is not None:
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


class RatingStrategy(IntentStrategy):
    def execute(self, entity):
        print("Entering Rating Strategy")
        if entity is None:
            return 'please type your question again'
        rating_query = db_commands.rating_query(entity)
        if rating_query is not None:
            rest_id = [elem['restaurant_id']for elem in rating_query]
            rating_list = [elem['star_rating']for elem in rating_query]
            overall_starrating = "The overall rating for " + \
                entity+" is " + str(rating_list[0])
        else:
            overall_starrating = "Sorry, There is no overall rating for this restaurant. Please try searching again"
        review_query = db_commands.user_rating_query(rest_id[0])
        if review_query is not None:
            user_review = [elem['review_content']for elem in review_query]
            user_rating = [elem['rating']for elem in review_query]
            user_starrating = "Here is a review from a visitor: " + \
                user_review[0] + "\nAnd the star rating the visitor gave for the restaurant: " + \
                str(user_rating[0])
        else:
            user_starrating = "Sorry, There are no reviews or ratings for this restaurant. Please try searching again"
        rating_response = overall_starrating+"\n"+user_starrating
        print(rating_response)
        return rating_response


class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name strategy')
        if entity is None:
            print('Sorry, please search again')

        foodtype_query = db_commands.food_type_query(entity)
        name_query = db_commands.name_search_query(entity)

        # check food type first
        if foodtype_query is not None:
            rest_list = [rest['restaurant_name'] for rest in foodtype_query]
            rest_list = rest_list[:3]

            results = ''
            for restaurant in rest_list:
                # rest_props = db_commands.name_search_query(entity)
                # rating = rest_props[0]['star_rating'] * '★'
                # results = results + restaurant + ' ' + rating
                results += restaurant + ', '            
            response = f'Here are some {entity} restaurants to check out: {results}'
            return response
            
        # then check is the entity is actually a restaurant name
        elif name_query is not None:
            rest_props = db_commands.rest_props_query(
                name_query[0]['restaurant_id'])

            # rest detail section
            location = rest_props[0]['city']
            price = rest_props[0]['price_range']
            rating = rest_props[0]['star_rating'] * '★'
            delivery = rest_props[0]['delivery_option']
            website = rest_props[0]['website']

            if type(delivery) != None and delivery == 1:
                delivery = "do"
            else:
                delivery = "don't"

            response = f'Here is some information we have on {entity} ({price},{rating})! \
                They are located in {location}, and do deliver. Find out more @ {website}'

            return response
        else:
            return "We couldn't find what you are looking for. Please be more specific and try searching again."


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


class UpdateStrategy(IntentStrategy):
    def execute(self, entity):
        print('update strategy')
        return 'Updating database with new results...'


class GratitudeStrategy(IntentStrategy):
    def execute(self, entity):
        print('gratitude' + entity)
        return 'gratitude ' + entity
