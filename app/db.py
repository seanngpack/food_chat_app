from flaskext.mysql import MySQL
import click
# from flask import current_app
from flask.cli import with_appcontext
from flask import Flask, request, Response


class DB:
    def __init__(self, db_name='HW4', user='root', db_host='localhost'):
        '''initialize the database object with database variables.

        '''

        self.db_name = db_name
        self.user = user
        self.db_host = db_host
        self.conn = None

    def initialize_db(self):
        '''Configure the MySql database for the flask application.

        '''

        from main import app  # get the application context.
        app.config['MYSQL_DATABASE_DB'] = self.db_name
        app.config['MYSQL_DATABASE_USER'] = self.user
        app.config['MYSQL_DATABASE_HOST'] = self.db_host
        mysql = MySQL()
        mysql.init_app(app)
        conn = mysql.connect()
        self.conn = conn

    def fetch_data(self, command):
        '''fetches data from the database based on what command you give it.

        Args:
            conn (Connection): Your db connection object.
            command (str): SQL command that fetches data you want to execute.

        Returns: 
            data from your command.

        '''

        cursor = self.conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        return data

    def create_db_schema(self, command):
        '''create a database schema.

        Args:
            command (str): the command you want to use to create the database schema with.

        TODO:
            fill out this method
        '''

        pass

    def close_db(self):
        '''closes your database connection.

        '''

        self.conn.close()

# TODO: add click command here to call create_db_schema
