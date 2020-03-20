import os
from flask import Flask, request, Response
from flaskext.mysql import MySQL
import json
import requests
from food_chat_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
