from flask import Blueprint,render_template,url_for,redirect,flash,request
from forms import SignupForm
from werkzeug.security import check_password_hash, generate_password_hash
from models import User,Userroles,Userrolesmapping
from ..extensions import db




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
			error="Passwords not matching."
		else:
			password_hash=generate_password_hash(password)
			data=User(email=email,password=password_hash)
			db.session.add(data)
			db.session.commit()

			userrole=Userroles.query.filter_by(role='User').first()
			user_role_mapping=Userrolesmapping(user_id=data.user_id,role_id=userrole.role_id)
			db.session.add(user_role_mapping)
			db.session.commit()
			
	
	return render_template('user_management/signup.html',form=form)



@user_management.route("forgotpassword",methods=['GET','POST'])
def forgotpassword():
	return render_template('user_management/forgotpassword.html')