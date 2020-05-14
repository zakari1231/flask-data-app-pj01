import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#db.init_app()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9'
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#SQLALCHEMY_TRACK_MODIFICATIONS = False
db.create_all()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
'''
    def __init__(self, username, full_name, email, password):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.password = password
   '''


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
'''
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author  
        self.year = year
'''


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text(), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



'''
    #username = db.Column("username", db.String, db.ForeignKey("users.username"))
    #full_name = db.Column("full_name", db.String, db.ForeignKey("users.full_name"))
    #isbn = db.Column("isbn", db.String, db.ForeignKey("books.isbn"))
    #title = db.Column("title", db.String, db.ForeignKey("books.title"))
    #author = db.Column("author", db.String, db.ForeignKey("books.author"))
    #year = db.Column("year", db.String, db.ForeignKey("books.year"))

    def __init__(self, rating, review, username, full_name, isbn, title, author, year):
        self.rating = rating
        self.review = review
        self.username = username
        self.full_name = full_name
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
'''  
    



   