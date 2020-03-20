from flaskext.mysql import MySQL
import click
from flask import current_app
from flask.cli import with_appcontext
from flask import Flask, request, Response
import json
import os
import requests


class Processor:
    '''This class processes JSON responses from the user and forms a suitable reply.
    '''

    def __init__(self, db):
        '''initialize the message processor.

        '''

        self.db = db
        self.response = None
        self.user_id = None
        self.user_message = None

    def reply(self, response):
        '''Processes the message and send a reply back to the user!

        Args:
            response: The JSON response

        '''

        for entry in response['entry']:
            try:
                self.load_user(entry)
                self.load_message(entry)
                return self.handle_message()
            except KeyError:
                # current_app.logger.warning(f"keyError in the response: {response}")
                pass
        return 'woops, something went wrong'

    def load_user(self, entry):
        '''get the username of the person the bot is talking to.

        Args:
            user (String): the user the bot is talking to
        '''

        user_id = entry['messaging'][0]['sender']['id']
        self.user_id = user_id

    def load_message(self, entry):
        '''get the user message from the response.

        Args:
            user (String): the user the bot is talking to
        '''

        self.user_message = entry['messaging'][0]['message']['text']

    def handle_message(self):
        '''This is where the message is broken down and interpreted.

        TODO:
            Add beef to this function, NLP, whatever.

        '''

        response = {
            'recipient': {'id': self.user_id},
            'message': {}
        }

        if self.user_message == 'fetch':
            data = self.db.fetch_data('SELECT * FROM EPL_stadiums')
            response['message']['text'] = str(data)
            return response
        else:
            response['message']['text'] = "Hello, you just sent me : " + \
                self.user_message
            return response

    def post_message(self, response):
        '''Posts a message

        Args:
            response: the JSON formatted response you want to post

        '''
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' +
            current_app.config['ACCESS_TOKEN'],
            json=response)
