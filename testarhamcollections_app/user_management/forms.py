from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField


class SignupForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm_Password")


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
