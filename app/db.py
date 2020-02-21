from flaskext.mysql import MySQL
import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    if 'db' not in g:
        mysql = MySQL()
        # current_app.config['MYSQL_DATABASE_USER'] = 'jay'
        # current_app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
        current_app.config['MYSQL_DATABASE_DB'] = 'HW4'
        current_app.config['MYSQL_DATABASE_USER'] = 'root'
        current_app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(current_app)
        conn = mysql.connect()
        g.db = conn

    return g.db

def fetch_test():
    '''do a cursor.execute command in here
    '''
    command = 'SELECT * FROM EPL_stadiums'
    cursor = g.db.cursor()
    cursor.execute(command)
    data = cursor.fetchall()
    print(data)
    return data


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(test_fetch_command)

@click.command('init-db')
@with_appcontext
def test_fetch_command():
    """start the database with flask and then do a fetch"""
    init_db()
    click.echo('Initialized the database.')
    fetch_test()

# TODO: missing init_db functions, implement later where the create table
# command is in sql and the init_db calls that sql file.