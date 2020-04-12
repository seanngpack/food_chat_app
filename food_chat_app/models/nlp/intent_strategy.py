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
            return 'Please type your question again'

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

            response = f'Here is some information I have on {entity} ({price},{rating})! \
                They are located in {location}, and do deliver. Find out more @ {website}'

            return response
        else:
            return "I couldn't find what you are looking for. Please be more specific and try searching again."


class RandomStrategy(IntentStrategy):
    def execute(self, entity):
        print('random stategy')
        random_query = db_commands.random_query()[0]
        
        name = random_query['restaurant_name']
        city = random_query['city']
        rating = random_query['star_rating'] * '★'
        price_range = random_query['price_range']
        reservation = random_query['reservation']
        vegan = random_query['vegan_option']
        delivery = random_query['delivery_option']
        website = random_query['website']

        response = f'How about {name} ({price_range},{rating})? \
            They are located in {city}, and do deliver. Find out more @ {website}'
        return response


class NullStrategy(IntentStrategy):
    def execute(self, entity):
        print('Null strat')
        return 'Sorry, please rephrase your question!'


class UpdateStrategy(IntentStrategy):
    def execute(self, entity):
        print('update strategy')
        return 'Updating database with new results...'


class GratitudeStrategy(IntentStrategy):
    def execute(self, entity):
        print('gratitude strat')
        responses = ['Happy to help!', 'You\'re welcome!', 'No problem',
        'Super, ask me more questions when you\'re ready!']
        return random.choice(responses)
