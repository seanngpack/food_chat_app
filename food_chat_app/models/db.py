from flaskext.mysql import MySQL
import click
# from flask import current_app
from flask.cli import with_appcontext
from flask import Flask, request, Response
from flask import current_app as app


db = MySQL()


class DB:
    def __init__(self):
        '''initialize the database object with database variables.

        '''
    
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

    def fetch_data(self, command):
        '''fetches data from the database based on what command you give it.

        Args:
            command (str): SQL command that fetches data you want to execute.

        Returns: 
            data from your command.

        '''

        self.cursor.execute(command)
        data = self.cursor.fetchall()
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
