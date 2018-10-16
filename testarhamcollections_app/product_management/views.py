from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify, session
# from models import ProductMaster
from models import VoteTest

from forms import AddProductForm, FormTest
from ..extensions import db
from werkzeug import secure_filename
import os
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
            return redirect(url_for('product_management.addproductimage', product_id=addproduct.product_id))
        return render_template("product_management/addproduct.html", form=form, product_id=product_id)

    else:
        productdata = ProductMaster.query.filter_by(product_id=product_id).first()
        form = AddProductForm(obj=productdata)
        form.populate_obj(productdata)
        if form.validate_on_submit():
            productdata.product_title = form.product_title.data
            db.session.add(productdata)
            db.session.commit()
            return redirect(url_for('product_management.addproductimage', product_id=product_id))
        return render_template("product_management/addproduct.html", form=form, product_id=product_id)


@product_management.route("addproductimage/<int:product_id>", methods=['POST', 'GET'])
def addproductimage(product_id):

    path = "/".join([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), "images", str(product_id)])

    if not os.path.exists(path):
        os.makedirs(path)

    for file in request.files.getlist('file'):
        filename = secure_filename(file.filename)
        destination = "/".join([path, filename])
        file.save(destination)

    return render_template("product_management/addproductimage.html", product_id=product_id)


@product_management.route("testjson/<int:id>", methods=['POST', 'GET'])
def testjson(id):
    list = [1, 2, 3]
    return jsonify(result=list)


@product_management.route('_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a * b)


@product_management.route("addnumberpage", methods=['POST', 'GET'])
def addnumberpage():
    form = FormTest()
    return render_template("product_management/addnumber.html", form=form)


@product_management.route('something', methods=['post'])
def something():
    form = FormTest()
    if form.validate_on_submit():
        str1 = form.name.data
        cnt = str1.upper()
        print
        return jsonify(data1={'message': 'hello {}'.format(cnt)})
    return jsonify(data1=form.errors)


@product_management.route('voteexample', methods=['POST', 'GET'])
def voteexample():
    vt = VoteTest.query.filter_by(voteid=1).first()
    return render_template("product_management/voteexample.html", vt=vt)


@product_management.route('changevote/<vote>', methods=['POST', 'GET'])
def changevote(vote=None):
    vt1 = request.args.get('vote')
    print "THIS IS VOTE {}".format(vt1)
    vt = VoteTest.query.filter_by(voteid=1).first()
    vt.votenumber = vt.votenumber + int(vote)
    db.session.add(vt)
    db.session.commit()
    return jsonify(data={'vote': vt.votenumber})


@product_management.route('testajax', methods=['POST', 'GET'])
def testajax():
    clicked = None
    
    if request.method == "POST":
        clicked = request.get_json()
        clicked['clicked'] = "test successul"
        if clicked == None:
            clicked = "test"
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX{}".format(clicked)
        return jsonify(data=clicked)
    return render_template("product_management/testajax.html")
