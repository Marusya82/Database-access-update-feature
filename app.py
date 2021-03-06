import peewee

from peewee import *
from flask import Flask

# create a web application with Flask
app = Flask(__name__)
#app.secret_key = ''

# create database instance
db = MySQLDatabase('your_database_name', **{'host': '127.0.0.1', 'user': 'root', 'passwd': 'your_password'})

'''
   this hook ensures that a connection is opened to handle any queries generated by the request
'''
@app.before_request
def _db_connect():
    db.connect()

'''
   this hook ensures that the connection is closed when we've finished processing the request
'''
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

