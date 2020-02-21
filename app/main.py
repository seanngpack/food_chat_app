from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

# TODO: abstract mysql configuration to a function
mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'sean'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'HW4'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM EPL_managers;")
print(cursor.values)

@app.route('/')
def hello():
    return 'Hello, World!'

print("HELLOASDDSAKJNAD!")