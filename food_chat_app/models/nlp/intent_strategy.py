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
        print('rating search' + entity)
        return 'rating search ' + entity


class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name strategy')

        if entity is None:
            return 'Please type your search again'

        name_query = db_commands.name_search_query(entity)
        if name_query is not None:
            rest_props = db_commands.rest_props_query(
                name_query[0]['restaurant_id'])
            review_props = db_commands.review_props_query(
                name_query[0]['restaurant_id'])
            hour_props = db_commands.hours_props_query(
                name_query[0]['restaurant_id'])
            initial_prompt = "Here is some information we have on: " + entity+". "

            # rest detail section
            location = rest_props[0]['city']
            avg_price = rest_props[0]['price_range']
            reservation = rest_props[0]['reservation']
            vegan = rest_props[0]['vegan_option']
            delivery = rest_props[0]['delivery_option']
            website = rest_props[0]['website']

            if type(delivery) != None and delivery == 1:
                delivery = "do"
            else:
                delivery = "don't"
            if type(reservation) != None and reservation == 1:
                reservation = "do take"
            else:
                reservation = "don't take"
            if type(vegan) != None and vegan == 1:
                vegan = "do have"
            else:
                vegan = "don't have"

            rest_details = "They are located in " + location + ", have an average price of " + avg_price + ", they " + delivery + \
                " deliver, " + reservation + " reservations and " + vegan + \
                " vegan options." + "Their website is: " + website + "! "

            # review section
            first_few_rev = []
            first_few_rate = []
            for index in range(len(review_props)-3):

                first_few_rev.append(review_props[index]['review_content'])
                first_few_rate.append(review_props[index]['rating'])

            results = "The reviews for " + entity + "are: " + \
                " and ".join(str(e) for e in first_few_rev) + " Rated at " + \
                " and ".join(str(e) for e in first_few_rate)+" stars."

            # hour section
            monday = hour_props[0]['monday_hours']
            tuesday = hour_props[0]['tuesday_hours']
            wednesday = hour_props[0]['wednesday_hours']
            thursday = hour_props[0]['thursday_hours']
            friday = hour_props[0]['friday_hours']
            open_times = "They are open from: " + monday+" on Monday, " + tuesday + " on Tuesday, " + \
                wednesday + " on Wednesday, "+thursday + \
                " on Thursday " + "and " + friday + " on Friday."

            return initial_prompt+rest_details+open_times+results

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
