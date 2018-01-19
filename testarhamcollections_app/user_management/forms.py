from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SelectField


class SignupForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm_Password")


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    gender = SelectField("Gender", choices=[('male', 'Male'), ('female', 'Female')])
    mobile_number = StringField("Contact No")
