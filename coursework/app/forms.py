from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from app.models import orders, User, stock, Concerts


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired(), Email()])
    password = PasswordField("Password*", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password*", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
    name = StringField("Name")
    address1 = StringField("Address 1")
    address2 = StringField("Address 2")
    towncity = StringField("Town/City")
    postcode = StringField("Postcode")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class EditForm(FlaskForm):
    email = StringField("Email")
    address1 = StringField("Address 1")
    address2 = StringField("Address 2")
    towncity = StringField("Town/City")
    postcode = StringField("Postcode")
    submit = SubmitField("Submit Changes")
    password = PasswordField("Password")
    password2 = PasswordField("Repeat Password", validators=[EqualTo("password")])
    og_password = PasswordField("Current Password", validators=[DataRequired()])
    name = StringField("Name")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")


class add_shows(FlaskForm):
    location = StringField("Location")
    # thedate = StringField("Date")
    venue = StringField("Venue")
    submit = SubmitField("Submit")
    day = SelectField(
        choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04"), ("05", "05"), ("06", "06"), ("07", "07"), ("08", "08"),
                 ("09", "09"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"),
                 ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"),
                 ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27"), ("28", "28"), ("29", "29"),
                 ("30", "30"), ("31", "31")])
    month = SelectField(
        choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04"), ("05", "05"), ("06", "06"), ("07", "07"), ("08", "08"),
                 ("09", "09"), ("10", "10"), ("11", "11"), ("12", "12")])
    year = SelectField(choices=[("2018", "2018"), ("2019", "2019"), ("2020", "2020"), ("2021", "2021")])


class edit_shows(FlaskForm):
    location = StringField("Location")
    venue = StringField("Venue")
    submit = SubmitField("Submit")
    day = SelectField(
        choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04"), ("05", "05"), ("06", "06"), ("07", "07"), ("08", "08"),
                 ("09", "09"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"),
                 ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"),
                 ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27"), ("28", "28"), ("29", "29"),
                 ("30", "30"), ("31", "31")])
    month = SelectField(
        choices=[("01", "01"), ("02", "02"), ("03", "03"), ("04", "04"), ("05", "05"), ("06", "06"), ("07", "07"), ("08", "08"),
                 ("09", "09"), ("10", "10"), ("11", "11"), ("12", "12")])
    year = SelectField(choices=[("2018", "2018"), ("2019", "2019"), ("2020", "2020"), ("2021", "2021")])
    the_list = [(None, "Select Show ID")]
    for i in Concerts.query.all():
        the_list.append((str(i.id), str(i.id)))
    show_id = SelectField(
        choices=the_list
    )


class edit_user_level(FlaskForm):
    the_list = [(None, "Select User")]
    for i in User.query.all():
        the_list.append((str(i.username), str(i.username)))
    username = SelectField(
        choices=the_list
    )
    accesslevel = SelectField(
        choices=[(None, "Select Access Level"), ("1", "1"), ("2", "2"), ("3", "3")]
    )
    password = PasswordField("Enter Your Password ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class add_to_cart(FlaskForm):
    size = SelectField(choices=[("Select Size", "Select Size"), ("S", "S"), ("M", "M"), ("L","L"), ("XL", "XL")])
    amount = SelectField(choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9")])
    submit = SubmitField("Add To Cart")


class add_item_to_store(FlaskForm):
    id = StringField("Item ID", validators=[DataRequired()])
    name = StringField("Item Name", validators=[DataRequired()])
    cat = StringField("Category", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    sale = StringField("Sale % (If Applicable)")
    image = StringField("Image Url (In Form images/folder/image)")
    back_image = StringField("2nd Image Url")
    size = StringField("Size")
    stock = StringField("Stock")
    colour = StringField("Colour")
    submit = SubmitField("Submit")
    catagory = SelectField(
        choices=[(None, "Select"), ("Mens", "Mens"), ("Womens", "Womens"), ("Outwear", "Outwear"), ("Accessories", "Accessories")]
    )

    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if id is not None:
            raise ValidationError("Please use a different Item ID.")


class checkout(FlaskForm):
    submit = SubmitField("Checkout")

class pay_money(FlaskForm):
    card = StringField("Card Number", validators=[DataRequired(), Length(min=16, max=16)])
    date = StringField("Expiry Date", validators=[DataRequired(), Length(min=5, max=5)])
    cvv = StringField("CVV", validators=[DataRequired(), Length(min=3, max=16)])
    submit = SubmitField("Next")

class topup_form(FlaskForm):
    the_list = [(None, "Select Item ID")]
    for i in stock.query.all():
        the_list.append((str(i.id), str(i.id)))
    item = SelectField(
        choices=the_list
    )
    amount = StringField("Amount Of Stock Added")
    submit = SubmitField("Submit")

class pay_form(FlaskForm):
    card = StringField("Card No.")
    date = StringField("Expiry Date")
    cvv = StringField("CVV")
    submit = SubmitField("Place Order")

class update_orders_form(FlaskForm):
    the_list = [(None, "Select Order ID")]
    for i in orders.query.all():
        the_list.append((str(i.order_id), str(i.order_id))) #TODO Use this in other places
    select = SelectField(
        choices=the_list
    )
    update = SelectField(
        choices=[(None, "Select Status"), ("Dispatched", "Dispatched"), ("Delivered", "Delivered")]
    )
    submit = SubmitField("Submit")
