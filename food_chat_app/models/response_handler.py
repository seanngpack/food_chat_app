from flaskext.mysql import MySQL
import click
from flask import current_app as app
from flask.cli import with_appcontext
from flask import Flask, request, Response
import json
import os
import requests


class ResponseHandler:
    '''This class processes responses from the user and forms a suitable reply.
    
    '''

    def __init__(self, db):
        '''initialize the message processor.

        '''

        self.db = db

    def get_reply(self, response):
        '''Processes the message and generates a reply.

        Args:
            response: The JSON response

        '''

        for entry in response['entry']:
            messaging = entry['messaging']
            for message in messaging:
                if message.get('message'):
                    user_id = message['sender']['id']
                    message_text = message['message'].get('text')
                    # if the user sends you a text message
                    if message_text:
                        return self.handle_message(user_id, message_text)



    def handle_message(self, user_id, sent_text):
        '''Helper method to get_reply, this is where the message 
        is broken down and interpreted.

        TODO:
            Add beef to this function, NLP, whatever.

        '''

        response = {
            'recipient': {'id': user_id},
            'message': {}
        }

        if sent_text == 'fetch':
            data = self.db.query('SELECT * FROM EPL_stadiums')
            response['message']['text'] = str(data)
            return response
        else:
            response['message']['text'] = "Hello, you just sent me : " + \
                sent_text
            return response

    def post_message(self, response):
        '''Posts a message.

        Args:
            response: the JSON formatted response you want to post

        '''
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' +
            app.config['ACCESS_TOKEN'],
            json=response)
