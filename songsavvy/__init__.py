from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdeac8f173801449a79cf1c89ab2b757'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db = SQLAlchemy(app)

from songsavvy import routes