from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emails = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(100), unique=True)
    emails = db.relationship('Emails')