from flask import Flask, request, Response
from flask import current_app as app
from food_chat_app.models.message.message_engine import MessageEngine
from food_chat_app.models.db.db import DB
from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp.intent_types import IntentType
from food_chat_app.models.nlp.intent_strategy import *
from food_chat_app.models.nlp import utils

db = DB()
message_engine = MessageEngine(db)
predictor = Predictor()


@app.route('/webhook', methods=['GET'])
def handle_verification():
    '''Verifies facebook webhook subscription.

    '''

    if request.args.get('hub.verify_token') == app.config['VERIFY_TOKEN']:
        app.logger.info('webhook verification success.')
        return request.args.get('hub.challenge')
    else:
        app.logger.error('webhook verification failed.')


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    '''Get user message, apply NLP to get the intent, then use the intent to
    formulate a response. Finally, send the response back to user.

    '''

    request_object = request.json
    if message_engine.parse_user_message(request_object) is not None:
        user_id, user_message = message_engine.parse_user_message(
            request_object)

        # get a named entity from the message
        chunked = utils.extract_entity(user_message)
        entity = utils.get_named_entity(chunked)

        # predict the user intent
        intentType = predictor.predict_intent(user_message)

        # get the intent and set the strategy of the MessageEngine
        message_engine.set_strategy(intentToStrat(intentType))

        # get a reply to the user message
        reply = message_engine.get_reply(user_id, entity)
        message_engine.post_message(reply)
        return Response(response="EVENT RECEIVED", status=200)
    return Response(response="EVENT RECEIVED", status=200)


def intentToStrat(intent: str):
    '''Given an IntentType, return a strategy for the MessageEngine

    Args:
        intent (IntentType): intent of the user message

    Returns:
        A strategy

    '''

    if intent == IntentType.restaurant_proximity_search:
        return ProximityStrategy()
    elif intent == IntentType.restaurant_food_type_search:
        return FoodTypeStrategy()
    elif intent == IntentType.restaurant_rating_search:
        return RatingStrategy()
    elif intent == IntentType.restaurant_search_by_name:
        return NameStrategy()
    elif intent == IntentType.restaurant_random_search:
        return RandomStrategy()
    elif intent == IntentType.restaurant_null_search:
        return NullStrategy()
    elif intent == IntentType.gratitude:
        return GratitudeStrategy()
