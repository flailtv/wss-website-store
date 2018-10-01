from app import app, db
from config import Config
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, EditForm, add_shows, edit_user_level, pay_money, add_to_cart, add_item_to_store, checkout, topup_form, pay_form, update_orders_form, edit_shows
from app.models import User, Concerts, Store, stock, orders, cart
from flask_login import current_user, login_user, logout_user, login_required
import arrow

# Fonts: Navbar- Century Gothic  Titles-Rockwell  Text-Myriad Pro

@app.route('/')
def index():
    return render_template("index.html", title="Home-")


@app.route("/about")
def about():
    return render_template("About.html", title="About-")


@app.route("/shows")
def shows():                                          ### shows html page ###
    current_date = arrow.now().format("YYYYMMDD")       # Parameters: None #
    for i in Concerts.query.all():                      # Return shows.html with the title "Shows" and passes in the Concerts Database #
        t = str(i.year) + str(i.month) + str(i.day)     # Purpose: To check the date and compare them against the shows int he concerts database. If the show has a date that has already happened, then it is deleted from the database. Then it presents the shows page on the website #
        if int(t) < int(current_date):
            db.session.delete(i)
            db.session.commit()
    return render_template("shows.html", title="Shows-", concerts=Concerts.query.all())


@app.route("/music")
def music():
    return render_template("Music.html", title="Music-")

@app.route("/photos")
def photos():
    return render_template("Photos.html", title="Photos-")

# Store Section

@app.route("/store")
def store():
    return render_template("store/store.html", title="Store-", store=Store.query.all())


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
    return render_template("store/accessories.html", title="Store-", store=Store.query.all())


@app.route("/store/cart", methods=["GET", "POST"])
@login_required
def the_cart():                                          ### Shopping Cart HTML Page ###
    final_price = 0                                        # Parameters: None #
    for j in cart.query.all():                             # Return: cart.html and passes the User, cart and store databases and the final price
        if current_user.id == j.userid:                    # Purpose: To display the the shopping cart of the logged in user. It also calculates the total price of all that user's items in the cart and passes it into the html file #
            the_price = int(j.price) * int(j.quantity)
            final_price = int(final_price) + int(the_price)
    return render_template("store/cart.html", title="Store-", users=User.query.all(), cart=cart.query.all(), store=Store.query.all(), final_price=final_price)


@app.route("/store/delivery")
@login_required
def delivery():
    return render_template("store/delivery.html", title="Store-", users=User.query.all())


@app.route("/store/pay", methods=["GET", "POST"])
@login_required
def pay():                                            ### Payment HTML File ###
    form = pay_money()                                  # Parameters: None #
    if form.validate_on_submit():                       # Return: pay.html file and passes in the pay_money() #
        for i in User.query.all():                      # Purpose: To display the payment html file and then redirects to confirmation screen when completed. It also saves the last 4 digits of the payment card to the database #
            if i.id == current_user.id:
                print(form.cvv.data)
                try:
                    if int(form.card.data):
                        if int(form.cvv.data):
                            card_no = str(form.card.data)
                            i.card = card_no[-5:-1]
                            db.session.commit()
                except:
                    flash("Card Number or CVV must be a number")
                    return render_template("store/pay.html", title="Store-", form=form)
        return redirect(url_for("confirmation"))
    return render_template("store/pay.html", title="Store-", form=form)


@app.route("/store/confirm", methods=["GET", "POST"])
@login_required
def confirmation():                                             ### Confirmation Page ###
    form = pay_form()                                             # Parameters: None #
    final_price = 0                                               # Returns: confirm.html and passes the cart, store and users databases, and the final price and pay_form #
    for j in cart.query.all():                                    # Purpose: To show the cart of the user checking out, their payment details and their address that the items are being shipped to. #
        if current_user.id == j.userid:                           # It shows the total price of the items and the shipping cost of the items. It also adds the items to the order list and remove said items from the cart. #
            the_price = int(j.price) * int(j.quantity)            # Finally, it sends out an email confirming your order #
            final_price = int(final_price) + int(the_price)
    final_price = int(final_price) + 4  #This makes the total amount from the items in the cart and adds the shipping cost (£4)
    if form.validate_on_submit():
        for i in cart.query.all():
            if current_user.id == i.userid:
                for j in stock.query.all():
                    if i.itemid == j.itemid:
                        j.stock = int(j.stock)-i.quantity
                        j.bought = int(j.bought) + int(i.quantity)
                        db.session.commit()
                current_date = arrow.now().format("DD-MM-YYYY")
                for user in User.query.all():
                    if user.id == current_user.id:
                        card_no = user.card
                        item = orders(userid=i.userid, item_id=i.itemid, item_quant=i.quantity, order_status="Processing", date=current_date, price=(int(i.price)*int(i.quantity)), card=card_no)
                        Config.server.sendmail("whileshesleeps.store.tester@gmail.com", i.email, "Your Order Has Been Placed")
                        db.session.add(item)   #adss items to order list
                        db.session.commit()
                        db.session.delete(i)   #removes items from cart
                        db.session.commit()
        flash("Order Has Been Placed")
        return redirect(url_for("store"))
    return render_template("store/confirm.html", title="Store-", cart=cart.query.all(), form=form, store=Store.query.all(), users=User.query.all(), final_price=final_price)


@app.route("/store/cart/wgbobgowubwnwhwpiew<the_cart_id>fgb3ighfvynotggb7gfb8ygfo8qgnf3rvyurywfry")  #removing item from cart
@login_required
def remove_item_cart(the_cart_id):             ### Remove item from cart ###
    for i in cart.query.all():                   # Parameters: None #
        if i.cart_id == int(the_cart_id):        # Returns: a redirect for the cart web page #
            if i.quantity == 1:                  # Purpose: To remove a specific item from the users cart, or lower the quantity of said item #
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
    return render_template("user/orders.html", title="Store-", store=Store.query.all(), orders=orders.query.all(), user=User.query.all())


@app.route("/admin/orders", methods=["GET", "POST"])
def order_page():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.id == current_user.id:
                if i.accesslevel >= 2:
                    form = update_orders_form()
                    if form.validate_on_submit():
                        for k in orders.query.all():
                            if int(k.order_id) == int(form.select.data):
                                k.order_status = form.update.data
                                db.session.commit()
                                for person in User.query.all():
                                    if person.id == k.userid:
                                        msg = "None"
                                        if str(form.update.data) == "Dispatched":
                                            msg = "Your Order Has Been Dispatched"
                                        elif str(form.update.data) == "Delivered":
                                            msg = "Your Order Has Been Delivered"
                                        Config.server.sendmail("whileshesleeps.store.tester@gmail.com", person.email, msg)
                                flash("Changes Made")
                    return render_template("user/admin/orders.html", title="Admin-", orders=orders.query.all(), users=User.query.all(), form=form)
                else:
                    return redirect(404)


@app.route("/store/item/<item_id>", methods=["GET", "POST"])
def store_item(item_id):
    the_item = Store.query.filter_by(id=item_id).first()
    form = add_to_cart()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            return redirect(url_for("login"))
        else:
            for i in stock.query.all():
                print("HGFUGUIF")
                if i.itemid == the_item.id:
                    if i.stock > 0:
                        for item1 in cart.query.all():
                            print("find")
                            if item1.userid == current_user.id:
                                if i.itemid == item1.itemid:
                                    print(i.itemid)
                                    item1.quantity = item1.quantity + 1
                                    db.session.commit()
                                    return render_template("store/store_item.html", title="Store-",store_item=the_item, store=Store.query.all(),stock=stock.query.all(), form=form, user=User.query.all())
                                else:
                                    print("HERE")
                        item = cart(userid=current_user.id, itemid=the_item.id, quantity=form.amount.data, price=the_item.price)
                        db.session.add(item)
                        db.session.commit()
                        flash("Item Has Been Added To Your Cart!")
                        break
                    else:
                        flash("There Is No Stock Available")
    return render_template("store/store_item.html", title="Store-", store_item=the_item, store=Store.query.all(), stock=stock.query.all(), form=form, user=User.query.all())


@app.route("/admin/additem")
def additem():
    form = add_item_to_store()
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if i.username == current_user.username:
                if i.accesslevel >= 2:
                    form = add_item_to_store()
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


@app.route("/admin/users", methods=["GET", "POST"])
def owner_user_access():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for j in User.query.all():
            if current_user.id == j.id:
                if j.accesslevel == 3:
                    form = edit_user_level()
                    if form.validate_on_submit():
                        for i in User.query.all():
                            if i.username == str(form.username.data):
                                i.accesslevel = form.accesslevel.data
                                db.session.commit()
                                flash("Changes Made")
                    return render_template("user/admin/all_users.html", title="Admin-", users=User.query.all(), form=form)


@app.route("/admin/shows", methods=["GET", "POST"])
def shows_page():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for j in User.query.all():
            if current_user.id == j.id:
                if j.accesslevel >= 2:
                    form = add_shows()
                    form2 = edit_shows()
                    if form.validate_on_submit():
                        show = Concerts(location=form.location.data, venue=form.venue.data, day=form.day.data, month=form.month.data, year=form.year.data)
                        db.session.add(show)
                        db.session.commit()
                        flash("Show Has Been Added")
                    if form2.validate_on_submit():
                        for i in Concerts.query.all():
                            if int(i.id) == int(form2.show_id.data):
                                i.location = form2.location.data
                                i.venue = form2.venue.data
                                i.day = form2.day.data
                                i.month = form2.month.data
                                i.year = form2.year.data
                                db.session.commit()
                                flash("Show Has Been Updated")
                    return render_template("user/admin/shows.html", title="Admin-", shows=Concerts.query.all(), form=form, form2=form2, users=User.query.all())
                else:
                    return redirect(404)

@app.route("/admin/stock", methods=["GET", "POST"])
def stock_page():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for i in User.query.all():
            if current_user.id == i.id:
                if i.accesslevel >= 2:
                    form = topup_form()
                    if form.validate_on_submit():
                        for j in stock.query.all():
                            if str(form.item.data) == str(j.id):
                                j.stock = j.stock + int(form.amount.data)
                                db.session.commit()
                                flash("Stock Updated")
                    return render_template("user/admin/stock.html", title="Admin-", stock=stock.query.all(), store=Store.query.all(), form=form, users=User.query.all())
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
        user = User(username=form.username.data, email=form.email.data, address1=form.address1.data, address2=form.address2.data, towncity=form.towncity.data, postcode=form.postcode.data, accesslevel=1, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You Are Now A Registered User!")
        return redirect(url_for("login"))
    return render_template("user/register.html", title="Register-", form=form)


@app.route("/user/<username>")
@login_required
def profile(username):
    return render_template("user/profile.html", title="Profile-", user=User.query.all(), the_username=username)


@app.route("/edit", methods=["GET", "POST"])
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


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if current_user.is_anonymous:
        return redirect(404)
    else:
        for o in User.query.all():
            if o.username == current_user.username:
                if o.accesslevel >= 2:
                    thedect = {}
                    thelist = []
                    for k in stock.query.all():
                        thedect[k] = (k.bought, k.id)
                    for j in thedect:
                        thelist.append(thedect[j])
                    thelist = sorted(thelist, reverse=True)
                    total_cost = 0
                    total_prof = 0
                    total_price = 0
                    for i in stock.query.all():
                        for j in Store.query.all():
                            if i.itemid == j.id:
                                ind_cost = j.cost * i.bought
                                ind_profit = j.price-j.cost
                                ind_profit1 = ind_profit*i.bought
                                total_cost += ind_cost
                                total_prof += ind_profit1
                                ind_price = j.price*i.bought
                                total_price += ind_price
                    return render_template("user/admin/admin_index.html", title="Admin-",  users=User.query.all(), store=Store.query.all(), stock=stock.query.all(), thelist=thelist, total_cost=total_cost, total_prof=total_prof, total_price=total_price)
                else:
                    return redirect(404)


@app.errorhandler(404)
def error_404():
    return render_template("error_pages/404.html"), 404


@app.errorhandler(500)
def error_500():
    db.session.rollback()
    return render_template("error_pages/500.html"), 500
