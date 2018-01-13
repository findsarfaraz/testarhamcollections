from flask import Blueprint,render_template,url_for,redirect,flash,request
from forms import SignupForm
from werkzeug.security import check_password_hash, generate_password_hash
from models import User,Userroles,Userrolesmapping
from ..extensions import db
from itsdangerous import URLSafeTimedSerializer
from ..extensions import mail
from flask_mail import Message
import random
import hashlib
from sqlalchemy import exc
import datetime




user_management=Blueprint('user_management',__name__,url_prefix="/",static_folder='./static',static_url_path="main_app/static",template_folder='./templates')
# from .extensions import db

@user_management.route("login",methods=['GET','POST'])
def login():
	return render_template('user_management/loginpage.html')


@user_management.route("signup",methods=['GET','POST'])
def signup():
	form=SignupForm()
	if form.validate_on_submit():
		email=form.email.data
		password=form.password.data
		confirm_password=form.confirm_password.data
		if password!=confirm_password:
			flash("ERROR! Passwords not matching.")
		else:
			try:
				salt = hashlib.sha1(str(random.random())).hexdigest()[:10] 
				password_hash=generate_password_hash(password+salt,'sha256')
				data=User(email=email,password=password_hash,email_salt=salt)
				db.session.add(data)
				db.session.commit()
				

				userrole=Userroles.query.filter_by(role='User').first()
				user_role_mapping=Userrolesmapping(user_id=data.user_id,role_id=userrole.role_id)
				db.session.add(user_role_mapping)
				db.session.commit()

				send_confirmation_email(email,salt)
			except exc.IntegrityError:
				db.session.rollback()
				flash('ERROR! Email ({}) already exists.'.format(form.email.data),'')
	return render_template('user_management/signup.html',form=form)



@user_management.route("forgotpassword",methods=['GET','POST'])
def forgotpassword():
	return render_template('user_management/forgotpassword.html')

@user_management.route("email",methods=['GET','POST'])
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
 
    msg = Message('Confirmation Email', sender = 'registration@arhamcollections.com', recipients =[user_email])
    msg.html=html
   
    mail.send(msg)

@user_management.route("confirm/<token>")
def confirm_email(token):
	print token
	try:
		confirm_serializer=URLSafeTimedSerializer.load('myprecious')
		email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=84600)
		print email
		print "test1"
		user=User.query.filter_by(email=email).first()
		print user.email

		if user.is_active:
			flash("Email is already confirmed")
		else:
			user.is_active=True
			user.confirmed_on=datetime.datetime.utcnow()
			db.session.add(user)
			db.session.commit()
			print "step1"
			flash("Thank you for confirming email")

	except:
		flash("this is so much fun")

	return redirect(url_for('main_app.home')) 


