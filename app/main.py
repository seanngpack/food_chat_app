from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


print("HELLOASDDSAKJNAD!")
