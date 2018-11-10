from flask import Blueprint, render_template, url_for, redirect, flash, request, current_app, session,abort,jsonify
from forms import SignupForm, LoginForm, ProfileForm, AddAddressForm, ChangePasswordForm, ForgotPasswordForm, PasswordResetForm
from werkzeug.security import check_password_hash, generate_password_hash
from models import (User, Userroles, Userrolesmapping, Userprofile, Useraddress
                    )
from ..extensions import db, login_manager

from itsdangerous import URLSafeTimedSerializer
from ..extensions import mail
from flask_login import login_user, logout_user, login_required, current_user


from flask_mail import Message
import random
import hashlib
from sqlalchemy import exc, and_, or_
import datetime
from flask_principal import identity_changed, AnonymousIdentity, Identity, Permission, RoleNeed, UserNeed
from collections import namedtuple
from flask_principal import identity_loaded
# from ..extensions import celery
# from celery.decorators import periodic_task
# from celery.task.schedules import crontab
import random 

from datetime import timedelta


user_management = Blueprint('user_management', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')
# from .extensions import db


app = current_app
admin_permission = Permission(RoleNeed('Admin'))
AddressNeed = namedtuple('AddressNeed', ['action', 'address_id'])


class AddressPermission(Permission):
    """Extend Permission to take a post_id and action as arguments"""

    def __init__(self, action, address_id=None):
        need = AddressNeed(action, address_id)
        # super(AddressPermission, self).__init__(need)
        super(AddressPermission, self).__init__(need)


@user_management.route("login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=="POST":
        x=request.form.to_dict()
        # print('THIS IS IS A USER {} '.format(x['email']))
        user = User.query.filter_by(email=x['email']).first()
        
        if user:
            if check_password_hash(user.password, x['password'] + user.email_salt):
                login_user(user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                return jsonify(success='logged in',redirect='/')
            else:
                return jsonify(error='Incorrect password')
        else:
            return jsonify(error='Username not registered')
    else:
        return render_template('user_management/loginpage.html', form=form)


@login_required
@user_management.route("logout")
def logout():

    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    identity_changed.send(current_app, identity=AnonymousIdentity())
    return redirect(url_for('main_app.home'))


@user_management.route("signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            flash("ERROR! Passwords not matching.")
            return render_template('user_management/signup.html', form=form)
        else:
            try:
                salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
                password_hash = generate_password_hash(password + salt, 'sha256')
                data = User(email=email, password=password_hash, email_salt=salt)
                db.session.add(data)
                db.session.commit()

                userrole = Userroles.query.filter_by(role='User').first()
                user_role_mapping = Userrolesmapping(user_id=data.id, role_id=userrole.role_id)
                db.session.add(user_role_mapping)
                db.session.commit()

                userprofile = Userprofile(user_id=data.id)
                db.session.add(userprofile)
                db.session.commit()

                send_confirmation_email(email)
            except exc.IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), '')
                return render_template('user_management/signup.html', form=form)
    return render_template('user_management/signup.html', form=form)


@user_management.route("email", methods=['GET', 'POST'])
def email():
    return render_template('user_management/email.html')


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for(
        'user_management.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'user_management/email.html',
        confirm_url=confirm_url)

    msg = Message('Confirmation Email', sender='registration@arhamcollections.com', recipients=[user_email])
    msg.html = html

    mail.send(msg)


@user_management.route("confirm/<token>")
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=84600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('user_management.login'))

    user = User.query.filter_by(email=email).first()

    if user.is_active:
        flash("Email is already confirmed, please login")
        return redirect(url_for('user_management.login'))
    else:
        user.is_active = True
        user.confirmed_on = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash("Thank you for confirming email")
        return redirect(url_for('user_management.login'))
    return redirect(url_for('user_management.login'))


@user_management.route("edituserprofile", methods=['GET', 'POST'])
@login_required
def edituserprofile():
    try:
        userprofile = Userprofile.query.filter_by(user_id=current_user.id).first()
        form = ProfileForm(obj=userprofile)
        form.populate_obj(userprofile)
    except:
        form=ProfileForm()

    if form.validate_on_submit():
        data=Userprofile(first_name=form.first_name.data,last_name=form.last_name.data,gender=form.gender.data,dateofbirth=form.dateofbirth.data,user_id=current_user.id)
        db.session.add(data)
        db.session.commit()
        return render_template('user_management/edituserprofile.html', form=form)
    return render_template('user_management/edituserprofile.html', form=form)


@user_management.route("accountpage", methods=['GET', 'POST'])
@login_required
def accountpage():
    return render_template('user_management/accountpage.html')


@user_management.route("addresslist", methods=['GET'])
@login_required
def addresslist():
    useraddress = Useraddress.query.filter(Useraddress.user_id == current_user.id).filter(Useraddress.delete_flag == 0).all()
    return render_template('user_management/addresslist.html', useraddress=useraddress)


@user_management.route('addaddress', methods=['GET', 'POST'])
@user_management.route("addaddress/<int:address_id>", methods=['GET', 'POST'])
@login_required
def addaddress(address_id=None):
    form = AddAddressForm()
    if request.method=='POST':
        x=request.form.to_dict()
        try:
            x['default_flag']
            x['default_flag']=True

        except:
            x['default_flag']=False

        if address_id==None:
            try:
                data = Useraddress(first_name=x['first_name'], last_name=x['last_name'], address1=x['address1'], address2=x['address2'], landmark=x['landmark'], state=x['state'], city=x['city'], pincode=x['pincode'], mobileno=x['mobileno'], default_flag=x['default_flag'],user_id=current_user.id)
                db.session.add(data)
                db.session.commit()
                if  x['default_flag']==True:
                    try:
                        defaultadddata=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id.address_id !=data.address_id).filter(Useraddress.default_flag==True).first()
                        defaultadddata.default_flag=False
                        db.session.commit()
                    except:
                        db.session.rollback()
                        return jsonify(error="You don't have any default adddress" )
                        # defaultadddata1=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id.address_id ==data.address_id).filter(Useraddress.default_flag==True).first()
                        # defaultadddata1.default_flag=True
                        # db.session.commit()
                return jsonify(success='Address Added Successfully')
            except:
                db.session.rollback()
                return jsonify(error='Error in adding Address')
        else:
            try:
               
                data=Useraddress.query.filter(db.and_(address_id ==address_id, Useraddress.user_id==current_user.id)).first()
                data.first_name=x['first_name']
                data.last_name=x['last_name']
                data.address1=x['address1']
                data.address2=x['address2']
                data.landmark=x['landmark']
                data.state=x['state']
                data.city=x['city']
                data.pincode=x['pincode']
                data.mobileno=x['mobileno']
                data.default_flag=x['default_flag']
                data.user_id=current_user.id
                db.session.add(data)
                db.session.commit()
                if  x['default_flag']==True:
                    try:
                        defaultadddata=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id!=address_id).filter(Useraddress.default_flag==True).first()
                        defaultadddata.default_flag=False
                        db.session.commit()
                        # defaultadddata1=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id==address_id).first()
                        # defaultadddata1.default_flag=True
                        # db.session.commit()
                    except:
                        print('THIS IS CURRENT {} WITH ADDRESS_ID {}'.format(address_id,current_user.id))
                        
                return jsonify(success='Address Updated Successfully')
            except:
                return jsonify(error='Address not found')
    else:
        if address_id==None:
            return render_template('user_management/addaddress.html', form=form,address_id=address_id)
        else:
            try:
                data=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id==address_id).first()
                form = AddAddressForm(obj=data)
                form.populate_obj(data)
                return render_template('user_management/addaddress.html', form=form,address_id=address_id)
            except:
                return redirect(404)
    return render_template('user_management/addaddress.html', form=form)


@user_management.route("deleteaddress/<int:address_id>", methods=['GET', 'POST'])
@login_required
def deleteaddress(address_id):
    ua = Useraddress.query.filter(Useraddress.address_id == address_id).first()
    ua.delete_flag = True
    db.session.add(ua)
    db.session.commit()
    return redirect(url_for('user_management.addresslist'))

    # return render_template('user_management/addresslist.html')


@user_management.route("changepassword", methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    user = User.query.filter_by(id=current_user.id).first()
    if request.method=='POST':
        x=request.form.to_dict()
        if check_password_hash(user.password, x['current_password'] + user.email_salt):
            if x['new_password'] ==x['confirm_password']:
                password_hash = generate_password_hash(x['new_password'] + user.email_salt, 'sha256')
                user.password = password_hash
                db.session.add(user)
                db.session.commit()
                return jsonify(success='Password Changed Successfully')
            else:
                return jsonify(error='New Password is not matching with Confirm Password')
        else:
            return jsonify(error='Inccorrect password')
    return render_template('user_management/changepassword.html', form=form)


@user_management.route("wishlist", methods=['GET', 'POST'])
def wishlist():
    return render_template('user_management/wishlist.html')


@user_management.route("forgotpassword", methods=['GET', 'POST'])
def forgotpassword():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email(form.email.data)
            flash("Password reset email sent, Please check your inbox")
        else:
            flash("email not registered with us")
            return redirect(url_for('user_management.signup'))
    return render_template('user_management/forgotpassword.html', form=form)


def send_password_reset_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for(
        'user_management.confirm_reset_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'user_management/email_password_reset.html',
        confirm_url=confirm_url)

    msg = Message('Password Reset Arhamollections.com', sender='registration@arhamcollections.com', recipients=[user_email])
    msg.html = html

    mail.send(msg)


@user_management.route("reset/<token>")
def confirm_reset_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=18000)
    except:
        flash('The confirmation link is invalid or has expired.', 'Error')
        return redirect(url_for('user_management.forgotpassword'))

    user = User.query.filter_by(email=email).first()

    if user:
        form = PasswordResetForm()
        if form.validate_on_submit():
            if form.new_password.data == form.confirm_password.data:
                password_hash = generate_password_hash(form.new_password.data + user.email_salt)
                user.password = password_hash
                db.session.add(user)
                db.session.commit()
                return redirect('user_management.login')
        return render_template('user_management/passwordreset.html', form=form)
    else:
        flash("User not in registered.")
        return redirect(url_for('user_management.signup'))
    return render_template('user_management/passwordreset.html', form=form)


@user_management.route("testprocedure", methods=['GET', 'POST'])
def testprocedure():
    y = ""
    x = dir(db.engine)
    for i in x:

        y = y + "<h1>" + i + "</h1>"
    # rl = db.session.execute('GET_USER_ROLE').fetchall()
    # print rl
    html = "<h1>" + y + "</h1>"

    return html


@user_management.route("testexecute", methods=['GET', 'POST'])
@login_required
def testexecute():
    user_id = 1
    parameter = 'set @user_id=' + str(current_user.id) + ";"
    sql = 'CALL GET_USER_ROLES ({0});'.format(user_id)
    x = db.engine.execute(sql)


    # print help(db.engine.execute)

    return "<h1>this is true</h1>"


@user_management.route("testexecute1", methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def testexecute1():
    user_id = 1
    parameter = 'set @user_id=' + str(current_user.id) + ";"
    sql = 'CALL GET_USER_ROLES (%s);'
    x = db.engine.execute(sql, user_id)

    # print help(db.engine.execute)

    return "<h1>this is true</h1>"


# @celery.task()
# def add_together(a, b):
#     y=datetime.datetime.now()
#     x="ran at {}: sum of {} & {} is {}".format(y,a,b,a+b)
#     return x

# @periodic_task(run_every=crontab(minute='*/1'))
# @celery.task()
# def run_add_together():
#     x=random.randint(10,1000)
#     y=random.randint(10,1000)
#     m=add_together(x,y)
#     return m

# @user_management.route("testcelery", methods=['GET', 'POST'])
# def testcelery():
#     x=random.randint(10,1000)
#     y=random.randint(10,1000)
#     add_together.delay(x, y)
 
#     return "rhis ran "




@user_management.route("addresstest/<int:address_id>", methods=['GET', 'POST'])
@login_required
def addresstest(address_id=None):
    x=Useraddress.query.filter(db.and_(address_id ==address_id, Useraddress.user_id==current_user.id)).first()
    print('THIS IS X {}'.format(x))
    # db.session.commit()
    # Useraddress.query.filter(address_id = address_id,user_id=current_user.id).update(dict(default_flag=True))
    # db.session.commit()
    return jsonify(data='Success')

