from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, EditForm, add_shows, edit_user_level, add_to_cart, add_item_to_store, checkout, topup_form
from app.models import User, Concerts, Store, stock, orders, cart, musicplayer
from flask_login import current_user, login_user, logout_user, login_required
import arrow

#TODO Add email comfirmation
#TODO Profits and Google Charts API
#TODO Add music_play to every single fucking thing
#TODO Add a payment thing

@app.route('/')
def index():
    return render_template("index.html", title="Home-")


@app.route("/about")
def about():
    return render_template("About.html", title="About-")


@app.route("/shows")
def shows():
    current_date = arrow.now().format("YYYYMMDD")
    for i in Concerts.query.all():
        t = str(i.year) + str(i.month) + str(i.day)
        if int(t) < int(current_date):
            db.session.delete(i)
            db.session.commit()
    return render_template("shows.html", title="Shows-", concerts=Concerts.query.all())


@app.route("/music")
def music():
    return render_template("Music.html", title="Music-", music_play=musicplayer.query.all())


@app.route("/store")
def store():
    return render_template("store/store.html", title="Store-")


@app.route("/photos")
def photos():
    return render_template("Photos.html", title="Photos-")

@app.route("/store/music")
def store_music():
    return render_template("store/music_store.html", title="Store-", store=Store.query.all())

@app.route("/store/mens")
def mens():
    return render_template("store/mens.html", title="Store-", store=Store.query.all())


@app.route("/store/outwear")
def outwear():
    return render_template("store/outwear.html", title="Store-", store=Store.query.all())


@app.route("/store/womens")
def womens():
    return render_template("store/womens.html", title="Store-", store=Store.query.all(), stock=stock.query.all())


@app.route("/store/accessories")
def accessories():
    return render_template("store/accessories.html", title="Store-")


@app.route("/store/cart", methods=["GET", "POST"])
@login_required
def the_cart():
    form = checkout()
    final_price = 0
    for j in cart.query.all():
        if current_user.id == j.userid:
            the_price = int(j.price) * int(j.quantity)
            final_price = int(final_price) + int(the_price)
    if form.validate_on_submit():
        for i in cart.query.all():
            if current_user.id == i.userid:
                for j in stock.query.all():
                    if i.itemid == j.itemid:
                        j.stock = int(j.stock) - (i.quantity)
                        db.session.commit()
                current_date = arrow.now().format("DD-MM-YYYY")
                item = orders(userid=i.userid, item_id=i.itemid, item_quant=i.quantity, order_status="Processing", date=current_date, price=i.price)
                db.session.add(item)
                db.session.commit()
                db.session.delete(i)
                db.session.commit()
        flash("Order Has Been Placed")
        return redirect(url_for("the_cart"))
    return render_template("store/cart.html", title="Store-", users=User.query.all(), cart=cart.query.all(), store=Store.query.all(), final_price=final_price, form=form)


@app.route("/store/cart/wgbobgowubwnwhwpiew<the_cart_id>fgb3ighfvynotggb7gfb8ygfo8qgnf3rvyurywfry")
@login_required
def remove_item_cart(the_cart_id):
    for i in cart.query.all():
        if i.cart_id == int(the_cart_id):
            if i.quantity == 1:
                db.session.delete(i)
                db.session.commit()
            else:
                i.quantity = i.quantity - 1
                db.session.commit()
    flash("Item Has Been Removed")
    return redirect((url_for("the_cart")))


@app.route("/store/orders")
@login_required
def the_orders():
    return render_template("store/orders.html", title="Store-", store=Store.query.all(), orders=orders.query.all(), user=User.query.all())


@app.route("/admin/orders")
def all_orders():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel >= 2:
                    return render_template("user/all_orders.html", title="Admin-", orders=orders.query.all())
#TODO Finish ALL Order Page


@app.route("/store/item/<item_id>", methods=["GET", "POST"])
def store_item(item_id):
    form = add_to_cart()
    the_item = Store.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            return redirect(url_for("login"))
        else:
            for i in stock.query.all():
                if i.itemid == the_item.id:
                    if i.stock > 0:
                        for item1 in cart.query.all():
                            if item1.userid == current_user.id:
                                if i.itemid == item1.itemid:
                                    item1.quantity = item1.quantity + 1
                                    db.session.commit()
                                    return render_template("store/store_item.html", title="Store-",store_item=the_item, store=Store.query.all(),stock=stock.query.all(), form=form, user=User.query.all())
                        item = cart(userid=current_user.id, itemid=the_item.id, quantity=form.amount.data, size=form.size.data, price=the_item.price)
                        db.session.add(item)
                        db.session.commit()
                        flash("Item Has Been Added To Your Cart!")
                    else:
                        flash("There Is No Stock Available")
    return render_template("store/store_item.html", title="Store-", store_item=the_item, store=Store.query.all(), stock=stock.query.all(), form=form, user=User.query.all())
#TODO Stop Items With No Stock Being Added To Cart


# @app.route("/store/item/<item_id>/edit", methods=["GET", "POST"])
# @login_required
# def item_admin_page():
#     for i in User.query.all():
#         if i.username == current_user.username:
#             if i.accesslevel >= 2:
#                 form =
#                 return render_template("user/change_user_level.html", title="Owner-", form = form)
#             else:
#                 return redirect(url_for(404))

@app.route("/admin/additem")
@login_required
def additem():
    form = add_item_to_store()
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel >= 2:
                    if form.validate_on_submit():
                        item = store(
                            id=int(form.id.data),
                            name=form.name.data,
                            image=form.image.data,
                            back_image=form.back_image.data,
                            cat=form.cat.data,
                            price=form.price.data,
                            sale=form.sale.data
                        )
                        db.session.add(item)
                        db.session.commit()
                        item = stock(
                            itemid=form.id.data,
                            size=form.size.data,
                            stock=form.stock.data,
                            colour=form.colour.data,
                        )
                        db.session.add(item)
                        db.session.commit()
                        flash("Item Added To The Store")

                else:
                    return redirect(url_for(404))
    return render_template("store/store_add.html", title="Admin-", form=form)


@app.route("/admin/topup", methods=["GET", "POST"])
def topup():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for j in User.query.all():
            if current_user.id == j.id:
                if j.accesslevel>= 2:
                    form = topup_form()
                    if form.validate_on_submit():
                        for i in stock.query.all():
                            if str(form.item.data) == str(i.id):
                                i.stock = i.stock + int(form.amount.data)
                                db.session.commit()
                                flash("Stock Updated")
                                # return render_template("user/topup.html", title="Admin", form=form)
                else:
                    return redirect(404)
    return render_template("user/topup.html", title="Admin", form=form)


@app.route("/admin/allstock", methods=["GET", "POST"])
def all_stock():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if current_user.id == i.id:
                if i.accesslevel >= 2:
                    return render_template("user/all_stock.html", title="Admin", stock=stock.query.all)
                else:
                    return redirect(404)


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
    return render_template("user/login.html", title="Login-", form=form)


@app.route("/logout")
@login_required
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
    return render_template("user/register.html", title="Register-", form=form)

@app.route("/user/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user/profile.html", title="Profile-", user=User.query.all())


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
    return render_template("user/edit_profile.html", title="Edit-", form=form)


@app.route("/shows/editshows")
def edit_shows():
    if current_user.is_anonymous:
        return redirect(404)
    return render_template("user/edit_shows.html", title="Shows-")


@app.route("/admin")
def admin():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel >= 2:
                    return render_template("user/admin.html", title="Admin-")
                else:
                    return redirect(404)


@app.route("/owner")
def owner():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel == 3:
                    return render_template("user/owner.html", title="Owner-")
                else:
                    return redirect(404)


@app.route("/admin/addshows", methods=["GET", "POST"])
def add_show():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel >= 2:
                    form = add_shows()
                    if form.validate_on_submit():
                        show = Concerts(location=form.location.data, venue=form.venue.data, day=form.day.data, month=form.month.data, year=form.year.data)
                        db.session.add(show)
                        db.session.commit()
                        flash("Show Has Been Added")
                        return redirect(url_for("add_show"))
                    return render_template("user/add_shows.html", title="Admin-", form=form)
                else:
                    return redirect(404)


@app.route("/owner/users")
def owner_users():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel == 3:
                    return render_template("user/all_users.html", title="Owner-", user = User.query.all())
                else:
                    return redirect(url_for("index"))


@app.route("/owner/edituser", methods=["GET", "POST"])
def edit_user_access_level():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel == 3:
                    form = edit_user_level()
                    for j in User.query.all():
                        if j.username == str(form.username.data):
                            j.accesslevel = form.accesslevel.data
                            db.session.commit()
                            flash("Changes Made")
                    return render_template("user/change_user_level.html", title="Owner-", form = form)
                else:
                    return redirect(404)


@app.errorhandler(404)
def error_404(error):
    return render_template("error_pages/404.html"), 404

@app.errorhandler(500)
def error_500(error):
    db.session.rollback()
    return render_template("error_pages/500.html"), 500
