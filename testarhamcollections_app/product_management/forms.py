from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, validators


class AddProductForm(FlaskForm):
    product_title = StringField("Product Title")


class FormTest(FlaskForm):
    name = StringField("name")


class AddMenuForm(FlaskForm):
    menu_name = StringField("menu_name")
    is_active = BooleanField("is_active")


class AddSubmenuForm(FlaskForm):
    submenu_name = StringField("submenu_name")
    is_active = BooleanField("is_active")
    menu_id = SelectField('menu_id', coerce=int)
