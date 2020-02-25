import os
from flask import Flask, request, Response
from flaskext.mysql import MySQL
import json
import requests


app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")  # webhook verification token


@app.route('/webhook', methods=['GET'])
def handle_verification():
    '''Verifies facebook webhook subscription.

    '''

    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Wrong validation token"


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        try:
            user_message = entry['messaging'][0]['message']['text']
            user_id = entry['messaging'][0]['sender']['id']
            response = {
                'recipient': {'id': user_id},
                'message': {}
            }
            response['message']['text'] = handle_message(user_message)
            requests.post(
                'https://graph.facebook.com/v2.6/me/messages/?access_token=' + ACCESS_TOKEN, json=response)
        except KeyError:
            app.logger.info(f"keyError in the response: {data}")
    return Response(response="EVENT RECEIVED", status=200)


def handle_message(user_message):
    '''Handle the message the user sent.

    Args:
        user_message (str): Message the user sent.

    Returns:
        A processed message to the user.
    
    TODO: Figure out how to map user_id to their actual names.

    '''
    return "Hello, you just sent me : " + user_message


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
