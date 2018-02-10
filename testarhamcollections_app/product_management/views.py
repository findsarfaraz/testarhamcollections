from flask import Blueprint, render_template, url_for, redirect, flash, request
from models import ProductMaster
from forms import AddProductForm
from ..extensions import db


product_management = Blueprint('product_management', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')
# from .extensions import db


@product_management.route("addproduct", methods=['POST', 'GET'])
@product_management.route("addproduct/<int:product_id>", methods=['POST', 'GET'])
def addproduct(product_id=None):
    if product_id == None:
        form = AddProductForm()
        if form.validate_on_submit():
            addproduct = ProductMaster(product_title=form.product_title.data)
            db.session.add(addproduct)
            db.session.commit()
            return redirect(url_for('product_management.addproductimage'))
            return render_template("product_management/addproduct.html", form=form, product_id=product_id)
    else:
        productdata = ProductMaster.query.filter_by(product_id=product_id).first()
        print "THIS IS PRODUCT DATA {}".format(productdata.product_id)
        form = AddProductForm(obj=productdata)
        form.populate_obj(productdata)
        if form.validate_on_submit():
            productdata.product_title = form.product_title.data
            db.session.add(productdata)
            db.session.commit()
            return redirect(url_for('product_management.addproductimage'))
    return render_template("product_management/addproduct.html", form=form, product_id=product_id)


@product_management.route("addproductimage", methods=['POST', 'GET'])
def addproductimage():
    return render_template("product_management/addproductimage.html")
