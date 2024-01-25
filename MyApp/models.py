from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, marshal_with, fields
from flask import request, current_app as app
import jwt
from functools import wraps
import datetime

app = Flask(__name__)
api = Api(app)


SECRET_KEY = 'abc123'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_occurrence_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(200), nullable=False)

class Incident(db.Model):
    incident_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    accused = db.Column(db.String(200), nullable=False)
    victim = db.Column(db.String(200), nullable=False)
    reported_by = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
