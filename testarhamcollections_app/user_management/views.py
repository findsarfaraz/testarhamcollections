from flask import Blueprint, render_template, url_for, redirect, flash, request
from forms import SignupForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Userroles, Userrolesmapping
from ..extensions import db, login_manager

from itsdangerous import URLSafeTimedSerializer
from ..extensions import mail
from flask_login import login_user, logout_user, login_required

from flask_mail import Message
import random
import hashlib
from sqlalchemy import exc
import datetime


user_management = Blueprint('user_management', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')
# from .extensions import db


@user_management.route("login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    print "started"
    if form.validate_on_submit():
        print "form valid"
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data + user.email_salt):
                login_user(user)
                flash("User logged in")
                return redirect(url_for('main_app.home'))
            else:
                flash("password not match")
        else:
            flash("User does not exists")

    return render_template('user_management/loginpage.html', form=form)


@user_management.route("logout")
def logout():
    logout_user()
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

                send_confirmation_email(email)
            except exc.IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), '')
    return render_template('user_management/signup.html', form=form)


@user_management.route("forgotpassword", methods=['GET', 'POST'])
def forgotpassword():
    return render_template('user_management/forgotpassword.html')


@user_management.route("email", methods=['GET', 'POST'])
def email():
    return render_template('user_management/email.html')


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer('myprecious')

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
        confirm_serializer = URLSafeTimedSerializer('myprecious')
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=84600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('user_management.login'))

    user = User.query.filter_by(email=email).first()

    if user.is_active:
        flash("Email is already confirmed")
    else:
        user.is_active = True
        user.confirmed_on = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash("Thank you for confirming email")

        return redirect(url_for('main_app.home'))
    return redirect(url_for('user_management.login'))


@user_management.route("userprofile")
@login_required
def userprofile():
    return render_template('user_management/userprofile.html')
