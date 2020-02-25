import os
from flask import Flask, request, Response
from flaskext.mysql import MySQL
import json
import requests
from db import DB


app = Flask(__name__)

# set access tokens
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")  # webhook verification token

# initialize our database
db = DB()
db.initialize_db()


@app.route('/webhook', methods=['GET'])
def handle_verification():
    '''Verifies facebook webhook subscription.

    '''

    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        app.logger.info('webhook verification success.')
        return request.args.get('hub.challenge')
    app.logger.info('webhook verification failed.')
    return "Wrong validation token"


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    '''When facebook pings us a post request, we get the response, unwrap it,
    process the info, and send a response back to facebook. This function is where we
    call the send_message() function to kick off processing the user's messages.

    '''

    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        try:
            user_message = entry['messaging'][0]['message']['text']
            user_id = entry['messaging'][0]['sender']['id']
            send_message(user_id, user_message)
        except KeyError:
            app.logger.warning(f"keyError in the response: {data}")
    return Response(response="EVENT RECEIVED", status=200)


def send_message(user_id, user_message):
    '''Send a message to the user based on their message.

    Args:
        user_id (str): user id of the sender.
        user_message (str): message they sent.

    '''

    response = {
        'recipient': {'id': user_id},
        'message': {}
    }
    if user_message == 'fetch':
        data = db.fetch_data('SELECT * FROM EPL_stadiums')
        app.logger.info(data)
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + ACCESS_TOKEN,
            json=response)
    else:
        response['message']['text'] = handle_message(user_message)
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + ACCESS_TOKEN,
            json=response)


def handle_message(user_message) -> str:
    '''Handles the message the user sent. This is where we want to add logic/processing to
    the users messages.

    Args:
        user_message (str): Message the user sent.

    Returns:
        A processed message to the user.

    TODO:
        1. Figure out how to use NLP 
        2. Use output from NLP to call on a DB query
        3. Construct DB query + statement in a helper function 
        4. Figure out how to map user_id to their actual names.

    '''
    return "Hello, you just sent me : " + user_message


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
