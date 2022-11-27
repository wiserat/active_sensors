from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(150), unique=True)
    emails = db.relationship('Email')
