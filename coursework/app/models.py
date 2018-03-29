from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return "<user {}>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(14))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def _repr__(self):
        return "<Post {}>".format(self.body)

class Concerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(40))
    venue = db.Column(db.String(40))
    date = db.Column(db.String(8))

    def __repr__(self):
        return "<Show ()>".format(self.location)