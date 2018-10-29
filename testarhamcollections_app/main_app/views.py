from flask import Blueprint, render_template, url_for, redirect, flash, request

from random import randint
main_app = Blueprint('main_app', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')
# from .extensions import db
from ..extensions import db
from ..models import Testset
from ..user_management.models import User, Userprofile, Userroles
from ..extensions import mail
from flask_mail import Message

# from ..app import allowed_file

from ..user_management.views import send_confirmation_email

from werkzeug.utils import secure_filename
import os


@main_app.route("/", methods=['GET', 'POST'])
def home():
    # send_confirmation_email('admin@arhamcollections.com')
    return render_template('main_app/index.html')
    # ,lsts=lsts,form=form,form1=form1)
    # return  "<h1>This is test</h1>"


@main_app.route("faq", methods=['GET', 'POST'])
def faq():

    # msg = Message('Hello', sender = 'registration@arhamcollections.com', recipients = ['findsarfaraz@gmail.com'])
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    return render_template('main_app/faq.html')


@main_app.route("create")
def create():
    db.create_all()
    return "all tables created"


@main_app.route("dropall")
def dropall():
    db.drop_all()
    return "all tables dropped"


@main_app.route("createroles")
def createroles():
    userroles = Userroles(role="Admin")
    db.session.add(userroles)
    db.session.commit()
    userroles = Userroles(role="User")
    db.session.add(userroles)
    db.session.commit()
    return "added all roles"


@main_app.route("imageupload", methods=['GET', 'POST'])
def imageupload():
    for file in request.files.getlist('file'):
        path = "/".join([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), "images"])
        print path
        filename = file.filename
        print filename
        destination = "/".join([path, filename])
        file.save(destination)

    return render_template('main_app/imageupload.html')


@main_app.route("testpath", methods=['GET', 'POST'])
def testpath():
    path = "/".join([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), "images"])
    print path
    return render_template('main_app/imageupload.html')

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @main_app.errorhandler(403)
# def page_not_found(e):
#     return render_template('403.html'), 403


# @main_app.errorhandler(410)
# def page_not_found(e):
#     return render_template('410.html'), 410


@main_app.route("admin", methods=['GET', 'POST'])
def admin():
    return render_template('main_app/admin.html')
