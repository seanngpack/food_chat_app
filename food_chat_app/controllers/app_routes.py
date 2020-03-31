from flask import Flask, request, Response
from flask import current_app as app
from food_chat_app.models.message.message_engine import MessageEngine
from food_chat_app.models.db.db import DB
from food_chat_app.models.nlp.predictor import Predictor

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
    '''When facebook pings us a request we unwrap it,
    process the info, and send a response back to facebook. 

    '''

    request_object = request.json
    if message_engine.get_reply(request_object) is not None:
        user_id, user_message = message_engine.parse_user_message(request_object)
        
        
        intent = predictor.predict_intent(user_message)
        #TODO: call the engine to convert intent to sql statement
        app.logger.info(user_message)
        reply = message_engine.handle_message(user_id, intent)
        message_engine.post_message(reply)
        return Response(response="EVENT RECEIVED", status=200)
    return Response(response="EVENT RECEIVED", status=200)
