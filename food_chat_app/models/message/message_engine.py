from flaskext.mysql import MySQL
from flask import current_app as app
from flask import Flask, request, Response
import json
import os
import requests


class MessageEngine:
    '''This class processes requests from the user and forms a suitable reply.

    '''

    def __init__(self):
        '''initialize the message processor.

        '''

        self.strategy = None

    def parse_user_message(self, request):
        '''Processes the message and generates a reply.

        Args:
            request: The JSON request

        '''

        for entry in request['entry']:
            messaging = entry['messaging']
            for message in messaging:
                if message.get('message'):
                    user_id = message['sender']['id']
                    message_text = message['message'].get('text')
                    # if the user sends you a text message
                    if message_text:
                        return user_id, message_text

    def get_reply(self, user_id, entity=None):
        '''Run strategy and get a response to the user.

        '''

        response = {
            'recipient': {'id': user_id},
            'message': {}
        }

        response['message']['text'] = self.strategy.execute(entity)
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

    def set_strategy(self, strategy):
        ''' given a strategy, set the strategy of this class 

        '''

        self.strategy = strategy
