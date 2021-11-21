from datetime import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")

    def __repr__(self):
        return f'User>>{self.username}'


class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=True)
    url = db.Column(db.Text(), nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return f'Bookmark>>{self.url}'

    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        picked_char = ''.join(random.choice(characters, k=3))
        link = self.query.filter_by(short_url=picked_char).first()
        if link:
            self.generate_short_characters()
        else:
            return picked_char
        

    def __init__(self, **kawargs):
        super().__init__(**kawargs)
        self.short_url = self.generate_short_characters()
