from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, RegisterForm, EditForm, add_shows
from app.models import User, Concerts, Store
from flask_login import current_user, login_user, logout_user, login_required


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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Login-", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, address1=form.address1.data, address2=form.address2.data, towncity=form.towncity.data, postcode=form.postcode.data, accesslevel = 1, name = form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You Are Now A Registered User!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register-", form=form)

@app.route("/user/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", title="Profile-", user=User.query.all())


@app.route("/edit", methods={"GET", "POST"})
@login_required
def edit_profile():
    form = EditForm(current_user.email)
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.address1 = form.address1.data
        current_user.address2 = form.address2.data
        current_user.towncity = form.towncity.data
        current_user.postcode = form.postcode.data
        current_user.name = form.name.data
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Password")
            return redirect(url_for("edit"))
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("edit_profile.html", title="Edit-", form=form)

@app.route("/shows/edit")
@login_required
def edit_shows():
    return render_template("edit_shows.html", title="Shows-", form=form)

@app.route("/admin")
@login_required
def admin():
    for i in User.query.all():
        if i.username == current_user.username:
            if i.accesslevel >= 2:
                return render_template("admin.html", title="Admin-")
            else:
                return redirect(url_for("index"))

@app.route("/owner")
@login_required
def owner():
    for i in User.query.all():
        if i.username == current_user.username:
            if i.accesslevel == 3:
                return render_template("owner.html", title="Owner-")
            else:
                return redirect(url_for("index"))

@app.route("/admin/editshows", methods=["GET", "POST"])
@login_required
def owner_page():
    for i in User.query.all():
        if i.username == current_user.username:
            if i.accesslevel >= 2:
                form = add_shows()
                if form.validate_on_submit():
                    show = Concerts(location=form.location.data, date=form.date.data, venue=form.venue.data, date_second=form.date_second.data)
                    db.session.add(show)
                    db.session.commit()
                    return redirect(url_for("edit_shows"))
                return render_template("edit_shows.html", title="Admin-", form=form)
            else:
                return redirect(url_for("profile"))