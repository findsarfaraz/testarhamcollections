from flask import Blueprint, render_template, url_for, redirect, flash, request, jsonify, session
from models import ProductMaster, MenuMaster, SubMenuMaster
from models import VoteTest
from flask_login import login_user, logout_user, login_required, current_user

from forms import AddProductForm, FormTest, AddMenuForm, AddSubmenuForm
from ..extensions import db
from werkzeug import secure_filename
import os
from flask_wtf.csrf import CsrfProtect

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
def changevote(vote):
    vt1 = request.args.get('vote')
    vt = VoteTest.query.filter_by(voteid=1).first()
    vt.votenumber = vt.votenumber + int(vote)
    db.session.add(vt)
    db.session.commit()
    return jsonify(data=vt.votenumber)


@product_management.route('testajax', methods=['POST', 'GET'])
def testajax():
    clicked = None
    if request.method == "POST":
        clicked = request.get_json()
        clicked['clicked'] = "test successul"
        if clicked == None:
            clicked = "test"
        return jsonify(data=clicked)
    return render_template("product_management/testajax.html")


# @product_management.route("addmenu", methods=['POST', 'GET'])
# @product_management.route("addmenu/<int:menu_id>", methods=['POST', 'GET'])
# def addmenu(menu_id=None):
#     if menu_id == None:
#         form = AddMenuForm()
#         if form.validate_on_submit():
#             addmenu = MenuMaster(menu_name=form.menu_name.data, is_active=form.is_active.data)
#             db.session.add(addmenu)
#             db.session.commit()
#             return redirect(url_for('main_app.admin'))
#         return render_template("product_management/addmenu.html", form=form, menu_id=menu_id)
#     else:
    # menudata = MenuMaster.query.filter_by(menu_id=menu_id).first()
    # form = AddMenuForm(obj=menudata)
    # form.populate_obj(menudata)
#         if form.validate_on_submit():
#             menudata.menu_name = form.menu_name.data
#             menudata.is_active = form.is_active.data
#             print("this is form is active data {}".format(form.is_active.data))
#             db.session.add(menudata)
#             db.session.commit()
#             return redirect(url_for('main_app.admin'))
#         return render_template("product_management/addmenu.html", form=form, menu_id=menu_id)


# @product_management.route("addsubmenu", methods=['POST', 'GET'])
# @product_management.route("addsubmenu/<int:submenu_id>", methods=['POST', 'GET'])
# def addsubmenu(submenu_id=None):
#     menulist = MenuMaster.query.all()
#     for i in menulist:
#         print(i)
#     if submenu_id == None:
#         form = AddSubmenuForm()
#         form.menu_id.choices = [(x.menu_id, x.menu_name) for x in MenuMaster.query.all()]
#         # print(dir(form.menu_id))
#         if form.validate_on_submit():
#             addsubmenu = SubMenuMaster(submenu_name=form.submenu_name.data, is_active=form.is_active.data, menu_id=form.menu_id.data)
#             db.session.add(addsubmenu)
#             db.session.commit()
#             # return render_template("product_management/addsubmenu.html", form=form, submenu_id=submenu_id, menulist=menulist)
#             return redirect(url_for('main_app.admin'))
#         return render_template("product_management/addsubmenu.html", form=form, submenu_id=submenu_id, menulist=menulist)
#         # return 'test'
#     else:
#         submenudata = SubMenuMaster.query.filter_by(submenu_id=submenu_id).first()
#         form = AddSubmenuForm(obj=submenudata)
#         form.menu_id.choices = [(x.menu_id, x.menu_name) for x in MenuMaster.query.all()]
#         form.populate_obj(submenudata)
#         if form.validate_on_submit():
#             submenudata.menu_name = form.submenu_name.data
#             submenudata.is_active = form.is_active.data
#             submenudata.menu_id = form.menu_id.data
#             db.session.add(submenudata)
#             db.session.commit()
#             return redirect(url_for('main_app.admin'))
#         return render_template("product_management/addsubmenu.html", form=form, submenu_id=submenu_id, menulist=menulist)


@product_management.route("menulist", methods=['POST', 'GET'])
def menulist():
    menulist = db.engine.execute('CALL GET_MENU_LIST')
    x = menulist.fetchall()
    print(x)
    return render_template('product_management/menulist.html', menulist=x)

    # try:
    #     menulist = db.engine.execute('CALL GET_MENU_LIST')
    #     rows=menulist.fetchall()
    #     print('THIS IS COUNT OF ROW {} '.format(rows.__len__()))
    #     if rows.__len__()>0:
    #         print('test')
    #         return render_template('product_management/menulist.html', menulist=rows)
    #     else:
    #         return redirect(url_for('product_management.addmenu', menu_id=None))
    # except:
    #     return redirect(url_for('product_management.addmenu', menu_id=None))
    # return render_template('product_management/menulist.html', menulist=rows)


@product_management.route("addmenu", methods=['POST', 'GET'])
@product_management.route("addmenu/<int:menu_id>", methods=['POST', 'GET'])
def addmenu(menu_id=None):
    if request.method == "POST":
        x = request.form.to_dict()
        try:
            x['is_active']
            x['is_active'] = True
        except KeyError:
            x['is_active'] = False
        if menu_id == None:
            try:
                menu = MenuMaster(menu_name=x['menu_name'], is_active=x['is_active'])
                db.session.add(menu)
                db.session.commit()
                return jsonify(success='Menu Added Successfully')
            except:
                error = 'Unable to add {}'.format(x['menu_name'])
                return jsonify(error=error)
        else:
            try:
                menu = MenuMaster.query.filter_by(menu_id=menu_id).first()
                menu.menu_name = x['menu_name']
                menu.is_active = x['is_active']
                db.session.add(menu)
                db.session.commit()
                return jsonify(success='Menu Updated Successfully')
            except:
                error = 'This record not found {}'.format(x['menu_name'])
                return jsonify(error=error)

    else:
        if menu_id == None:
            form = AddMenuForm()
            return render_template('product_management/addmenu.html', menu_id=menu_id, form=form)
        else:
            form = AddMenuForm()
            try:
                menudata = MenuMaster.query.filter_by(menu_id=menu_id).first()
                form = AddMenuForm(obj=menudata)
                form.populate_obj(menudata)
                return render_template('product_management/addmenu.html', menu_id=menu_id, form=form)
            except:
                return redirect(404)


@product_management.route('addsubmenu', methods=['POST', 'GET'])
@product_management.route("addsubmenu/<int:submenu_id>", methods=['POST', 'GET'])
def addsubmenu(submenu_id=None):
    form = AddSubmenuForm()
    menulist = MenuMaster.query.all()
    if request.method == "POST":
        x = request.form.to_dict()
        try:
            x['is_active']
            x['is_active'] = True
        except KeyError:
            x['is_active'] = False
        if submenu_id == None:
            try:
                submenumaster = SubMenuMaster(submenu_name=x['submenu_name'], is_active=x['is_active'], menu_id=x['menu_id'])
                db.session.add(submenumaster)
                db.session.commit()
                return jsonify(success='Submenu Added Successfully')
            except:
                return jsonify(error='Submenu Addition Failed')
        else:
            try:
                submenudata = SubMenuMaster.query.filter_by(submenu_id=submenu_id).first()
                submenudata.submenu_name = x['submenu_name']
                submenudata.is_active = x['is_active']
                submenudata.menu_id = x['menu_id']
                db.session.add(submenudata)
                db.session.commit()
                return jsonify(success='Submenu Updated Successfully')
            except:
                return jsonify(error='Unable to fetch data')
    else:
        if submenu_id == None:
            return render_template('product_management/addsubmenu.html', submenu_id=submenu_id, form=form, menulist=menulist)
        else:
            try:
                submenudata = SubMenuMaster.query.filter_by(submenu_id=submenu_id).first()
                form = AddSubmenuForm(obj=submenudata)
                form.populate_obj(submenudata)
                return render_template('product_management/addsubmenu.html', submenu_id=submenu_id, form=form, menulist=menulist)
            except:
                return redirect(404)
                # return jsonify(error='Unable to fetch data')
