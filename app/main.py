import os
from flask import Flask, request, Response
from flaskext.mysql import MySQL
import json
import requests
from db import DB
from processor import Processor


app = Flask(__name__)

# set access tokens
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")  # webhook verification token

# initialize our database
db = DB()
db.initialize_db()

# initialize our message processor
processor = Processor(db)



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
    process the info, and send a response back to facebook. 

    '''

    data = json.loads(request.data.decode('utf-8'))

    reply = processor.reply(data)
    post_message(reply)
    return Response(response="EVENT RECEIVED", status=200)

def post_message(response):
    '''Posts a message

    Args:
        response: the JSON formatted response you want to post

    '''

    requests.post(
                'https://graph.facebook.com/v2.6/me/messages/?access_token=' + ACCESS_TOKEN,
                json=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
