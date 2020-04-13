from flask import Flask, request, Response
from flask import current_app as app
from food_chat_app.models.message.message_engine import MessageEngine
from food_chat_app.models.db.db import DB
from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp.intent_types import IntentType
from food_chat_app.models.nlp.intent_strategy import *
from food_chat_app.models.nlp import utils
from food_chat_app.models.db.commands import insert_user
from food_chat_app.models.db.commands import insert_message

message_engine = MessageEngine()
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
        message_engine.set_strategy(intent_to_strat(intentType))

        # get a reply to the user message
        reply = message_engine.get_reply(user_id, entity)
        message_engine.post_message(reply)

        # store the user message
        insert_user(user_id)
        insert_message(user_id, user_message)

        return Response(response="EVENT RECEIVED", status=200)
    return Response(response="EVENT RECEIVED", status=200)


def intent_to_strat(intent: str):
    '''Given an IntentType, return a strategy for the MessageEngine

    Args:
        intent (IntentType): intent of the user message

    Returns:
        A strategy

    '''

    if intent == IntentType.restaurant_proximity_search:
        return ProximityStrategy()
    elif intent == IntentType.restaurant_rating_search:
        return RatingStrategy()
    elif intent == IntentType.restaurant_search_by_name:
        return NameStrategy()
    elif intent == IntentType.restaurant_random_search:
        return RandomStrategy()
    elif intent == IntentType.restaurant_null_search:
        return NullStrategy()
    elif intent == IntentType.update_database:
        return UpdateStrategy()
    elif intent == IntentType.delete:
        return DeleteStrategy()
    elif intent == IntentType.gratitude:
        return GratitudeStrategy()
