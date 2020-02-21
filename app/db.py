from flaskext.mysql import MySQL
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        mysql = MySQL()
        # current_app.config['MYSQL_DATABASE_USER'] = 'jay'
        # current_app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
        current_app.config['MYSQL_DATABASE_DB'] = 'HW4'
        current_app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        conn = mysql.connect()
        g.db = conn
        g.db.cursor = conn.cursor

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)

# TODO: missing init_db functions, implement later where the create table
# command is in sql and the init_db calls that sql file.