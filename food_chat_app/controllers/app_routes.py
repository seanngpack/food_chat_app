from flask import Flask, request, Response, current_app
from food_chat_app.models.response_handler import ResponseHandler
from food_chat_app.models.db import DB
import json

db = DB()
response_handler = ResponseHandler(db)

@current_app.route('/webhook', methods=['GET'])
def handle_verification():
    '''Verifies facebook webhook subscription.

    '''
    
    if request.args.get('hub.verify_token') == current_app.config['VERIFY_TOKEN']:
        current_app.logger.info('webhook verification success.')
        return request.args.get('hub.challenge')
    current_app.logger.info('webhook verification failed.')
    return "Wrong validation token"


@current_app.route('/webhook', methods=['POST'])
def handle_webhook():
    '''When facebook pings us a post request, we get the response, unwrap it,
    process the info, and send a response back to facebook. 

    '''

    data = json.loads(request.data.decode('utf-8'))

    reply = response_handler.reply(data)
    response_handler.post_message(reply)
    return Response(response="EVENT RECEIVED", status=200)