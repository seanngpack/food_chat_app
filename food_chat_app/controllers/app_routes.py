from flask import Flask, request, Response
from flask import current_app as app
from food_chat_app.models.message.message_engine import MessageEngine
from food_chat_app.models.db.db import DB

db = DB()
message_engine = MessageEngine(db)


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
    reply = message_engine.get_reply(request_object)
    message_engine.post_message(reply)
    return Response(response="EVENT RECEIVED", status=200)
