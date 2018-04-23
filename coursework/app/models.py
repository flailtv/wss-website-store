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
    name = db.Column(db.String(40), index = True)
    address1 = db.Column(db.String(40), index=True)
    address2 = db.Column(db.String(40), index=True)
    towncity = db.Column(db.String(40), index=True)
    postcode = db.Column(db.String(40), index=True)
    accesslevel = db.Column(db.Integer, index=True)

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
    thedate = db.Column(db.Date)
    date_second = db.Column(db.Date)

    def __repr__(self):
        return "<Show ()>".format(self.location)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    image = db.Column(db.String(40))
    cat = db.Column(db.String(40))
    price = db.Column(db.Float)
    sale = db.Column(db.Integer)
    size = db.Column(db.String(40))
    stock = db.Column(db.Integer)


class orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer)
    item_quant = db.Column(db.Integer)
    order_status = db.Column(db.String(40))

