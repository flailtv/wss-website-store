from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    address1 = db.Column(db.String(40), index=True, unique=True)
    address2 = db.Column(db.String(40), index=True, unique=True)
    towncity = db.Column(db.String(40), index=True, unique=True)
    postcode = db.Column(db.String(40), index=True, unique=True)

    def __repr__(self):
        return "<user {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

