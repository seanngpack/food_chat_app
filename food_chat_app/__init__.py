import os

from flask import Flask
from flaskext.mysql import MySQL


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from food_chat_app.models.db.db import db
    db.init_app(app)

    with app.app_context():
        from food_chat_app.controllers import app_routes
        return app
