from config import Config
import pymysql

'''File that builds the database

'''

config = Config()
conn = pymysql.connect(host=config.MYSQL_DATABASE_HOST,
                       user=config.MYSQL_DATABASE_USER,
                       password='',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


def get_sql_commands_from_file(sql_file: str):
    '''Given a file, loads the sql statements delineated by ;

    Args:
        sql_file (str): the file path of the file

    Returns:
        a list of the sql commands in the file

    '''

    with open(sql_file) as file:
        text = file.read()
        sql_commands = [x.replace('\n', '') for x in text.split(';') if x]
        return sql_commands


def create_db():
    '''Creates a database if it doesn't exist yet!

    '''
    global conn
    list_db = cursor.execute("SHOW DATABASES")
    list_db = cursor.fetchall()
    for entry in list_db:
        if entry['Database'] == 'food_chat_db':
            print('database already exists, maybe you want to drop it instead')
            return

    
    sql_commands = get_sql_commands_from_file('sql/create_all_tables.sql')
    for cmd in sql_commands:
        cursor.execute(cmd)
    conn.commit()
    print('built new database!')


if __name__ == '__main__':
    create_db()
