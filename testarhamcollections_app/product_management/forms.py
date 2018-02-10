from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField


class AddProductForm(FlaskForm):
    product_title = StringField("Product Title")
