from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, RegisterForm
from datashows import Shows
from app.models import User, Post, Concerts
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def index():
    return render_template("index.html", title="Home-")


@app.route("/about")
def about():
    return render_template("About.html", title="About-")


@app.route("/shows")
def shows():
    return render_template("shows.html", title="Shows-", Shows=Shows(), concerts=Concerts.query.all())


@app.route("/music")
def music():
    return render_template("Music.html", title="Music-")


@app.route("/store")
def store():
    return render_template("store/store.html", title="Store-")


@app.route("/photos")
def photos():
    return render_template("Photos.html", title="Photos-")


@app.route("/store/shirts")
def shirts():
    return render_template("store/shirts.html", title="Store-")


@app.route("/store/outwear")
def outwear():
    return render_template("store/outwear.html", title="Store-")


@app.route("/store/womens")
def womens():
    return render_template("store/womens.html", title="Store-")


@app.route("/store/accessories")
def accessories():
    return render_template("store/accessories.html", title="Store-")


@app.route("/store/cart")
def cart():
    return render_template("store/cart.html", title = "Store-")


@app.route("/about/taylor")
def tatylor():
    return render_template("about/taylor.html", title = "About-")


@app.route("/about/long")
def long():
    return render_template("about/long.html", title = "About-")


@app.route("/about/welsh")
def welsh():
    return render_template("about/long.html", title = "About-")


@app.route("/about/mckenzie")
def mckenzie():
    return render_template("about/mckenzie.html", title ="About-")


@app.route("/about/savage")
def savage():
    return render_template("about/savage.html", title = "About-")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect( "/" )
    return render_template("login.html", title="Login-", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, address1=form.address1.data, address2=form.address2.data, towncity=form.towncity.data, postcode=form.postcode.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You Are Now A Registered User!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register-", form=form)