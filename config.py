import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    '''General flask variables'''
    # DEBUG = True
    # DEVELOPMENT = True
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")  # webhook verification token

    '''DB variables'''
    MYSQL_DATABASE_DB = os.environ.get('DB_NAME')
    MYSQL_DATABASE_USER = os.environ.get('DB_USER')
    MYSQL_DATABASE_HOST = os.environ.get('DB_HOST')
