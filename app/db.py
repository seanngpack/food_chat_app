from flaskext.mysql import MySQL
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db(db_name='HW4', user='root', db_host='localhost'):
    '''initalizes the mySql database using the shared application instance. 
    Also stores the database connection into request object g.

    Args:
        db_name (str): name of the database you want to connect to.
        user (str): name of the user connecting.
        db_host (str): host address of the database you are connecting to.

    '''

    if 'db' not in g:
        mysql = MySQL()
        current_app.config['MYSQL_DATABASE_DB'] = db_name
        current_app.config['MYSQL_DATABASE_USER'] = user
        current_app.config['MYSQL_DATABASE_HOST'] = db_host
        mysql.init_app(current_app)
        conn = mysql.connect()
        g.db = conn

    return g.db

def fetch_data(command):
    '''fetches data from the database based on what command you give it.

    Args:
        command (str): SQL command that fetches data you want to execute.

    Returns: 
        data from your command.

    '''

    cursor = g.db.cursor()
    cursor.execute(command)
    data = cursor.fetchall()
    return data

def create_db_schema(command):
    '''create a database schema.

    Args:
        command (str): the command you want to use to create the database schema with.
    '''

    pass


def close_db(e=None):
    '''closes your database connection.

    '''

    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(test_fetch_command)

#TODO: later create an init-db click command to initialize a databse using 'flask init-db'

@click.command('fetch-data')
@with_appcontext
def test_fetch_command():
    '''initializes the database connection and executes your SQL query.

    Usage:
        run with `flask fetch-data`

    '''

    get_db()
    click.echo('Initialized the database.')
    data = fetch_data('SELECT * FROM EPL_stadiums')
    print(data)
