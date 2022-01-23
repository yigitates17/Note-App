from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    data = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    birthday = db.Column(db.Date)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')


class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[
        validators.Length(message="Title can't be shorter than 3 characters.", min=3)])
    content = TextAreaField('Note', validators=[
        validators.Length(message="Note can't be shorter than 3 characters.", min=3)])
