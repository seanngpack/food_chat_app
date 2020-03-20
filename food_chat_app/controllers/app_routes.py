from flask import Flask, request, Response
from flask import current_app as app
from food_chat_app.models.response_handler import ResponseHandler
from food_chat_app.models.db import DB
from pprint import pformat

db = DB()
response_handler = ResponseHandler(db)

@app.route('/webhook', methods=['GET'])
def handle_verification():
    '''Verifies facebook webhook subscription.

    '''
    
    if request.args.get('hub.verify_token') == app.config['VERIFY_TOKEN']:
        app.logger.info('webhook verification success.')
        return request.args.get('hub.challenge')
    else:
        app.logger.info('webhook verification failed.')
        

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    '''When facebook pings us a post request, we get the response, unwrap it,
    process the info, and send a response back to facebook. 

    '''
    
    request_object = request.json
    reply = response_handler.get_reply(request_object)
    response_handler.post_message(reply)
    return Response(response="EVENT RECEIVED", status=200)