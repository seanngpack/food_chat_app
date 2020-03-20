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

        self._conn = db.connect()
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        '''Commit changes to the db.

        '''

        self.connection.commit()

    def execute(self, sql, params=None):
        '''Execute the sql command.

        '''

        self.cursor.execute(sql, params or ())

    def fetchall(self):
        '''Fetch the results from your sql command.

        '''

        return self.cursor.fetchall()

    def fetchone(self):
        '''Fetch just one result of your sql command.

        '''

        return self.cursor.fetchone()

    def query(self, sql, params=None):
        '''Execute and fetch results of your sql command. You can pass in params
        to the SQL query, or form the params in the sql query itself. Your call.

        Args:
            sql (String): The sql query you want to run.
            params: Any additional parameters for the query.

        Returns:
            The result of your query.

        Example: 
            sql = "SELECT * FROM transactions WHERE transaction_date = ?"
            self.query(sql, (date,))

        '''

        self.cursor.execute(sql, params or ())
        return self.fetchall()


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

        self._conn.close()
