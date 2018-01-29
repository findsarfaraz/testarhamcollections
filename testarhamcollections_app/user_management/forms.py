from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField


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
    dateofbirth = DateField("Date Of Birth", format='%d/%m/%Y')


class AddAddressForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    address1 = StringField("Address1")
    address2 = StringField("Address2")
    landmark = StringField("Land Mark")
    state = StringField("State")
    city = StringField("City")
    pincode = StringField("Pin Code")
    mobileno = StringField("Mobile No")
    default_flag = BooleanField("Default Flag")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password")
    new_password = PasswordField("New Password")
    confirm_password = PasswordField("Confirm Password")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Registered Email")


class PasswordResetForm(FlaskForm):
    new_password = PasswordField("New Password")
    confirm_password = PasswordField("Confirm Password")
