from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(40), index=True)
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


class Concerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(40))
    venue = db.Column(db.String(40))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)


@login.user_loader
def load_user(the_id):
    return User.query.get(int(the_id))


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    image = db.Column(db.String(40))
    cat = db.Column(db.String(40))
    price = db.Column(db.Float)
    sale = db.Column(db.Integer)
    back_image=db.Column(db.String)


class stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemid = db.Column(db.Integer, db.ForeignKey("store.id"))
    size = db.Column(db.String(40))
    stock = db.Column(db.Integer)
    colour = db.Column(db.String(40))
    bought = db.Column(db.Integer)


class orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    item_quant = db.Column(db.Integer)
    order_status = db.Column(db.String(40))
    date = db.Column(db.String)
#TODO As Soon As I Added Date It Went Tits Up


class cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    itemid = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    size = db.Column(db.String)


class musicplayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.Integer)
    name = db.Column(db.String)
    album = db.Column(db.String)
    file = db.Column(db.String)
