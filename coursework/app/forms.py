from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


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
    og_password = PasswordField("Current Password", validators=[DataRequired])


    def __init__(self,og_email, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.og_email = og_email


    def validate_email(self, email):
        if email.data != self.og_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError("Please use a different email address.")
