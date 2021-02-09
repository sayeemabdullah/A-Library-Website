from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

# import os

app = Flask(__name__)

# file_path = os.path.abspath(os.getcwd())+"\alw.db"

app.config['SECRET_KEY'] = 'xxxx'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\A-Library-Website\\alw.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    publication_year = db.Column(db.Integer)

class Wishlist(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)



if __name__ == '__main__':
    app.run(debug=True)