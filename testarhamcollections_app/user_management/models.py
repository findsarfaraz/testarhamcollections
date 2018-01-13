
from  ..extensions import db
import datetime



class User(db.Model):
	
	__tablename__ = 'user'
	
	user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	email=db.Column(db.String(80), unique=True,nullable=False)
	mobile_login=db.Column(db.String(15),unique=True,nullable=True)
	password=db.Column(db.String(256),nullable=False)
	creation_date=db.Column(db.DateTime,default=datetime.datetime.utcnow())
	updation_date=db.Column(db.DateTime,onupdate=datetime.datetime.utcnow())
	is_active=db.Column(db.Boolean,default=False)	
	userprofiles=db.relationship("Userprofile",uselist=False, backref='user', lazy=True)
	useraddresses=db.relationship("Useraddress",backref="user",lazy=True)
	email_salt=db.Column(db.String(256),nullable=False)
	confirmed_on=db.Column(db.DateTime)

class Userprofile(db.Model):

	__tablename__='userprofile'
	
	profile_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	first_name=db.Column(db.String(50))
	last_name=db.Column(db.String(50))
	gender=db.Column(db.String(6))
	mobile_number=db.Column(db.String(15))
	creation_date=db.Column(db.DateTime,default=datetime.datetime.utcnow())
	updation_date=db.Column(db.DateTime,onupdate=datetime.datetime.utcnow())
	activation_key=db.Column(db.String(512))
	key_expires =db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class Useraddress(db.Model):
	
	__tablename__='useraddress'
	
	address_id =db.Column(db.Integer,primary_key=True, autoincrement=True)
	first_name=db.Column(db.String(50))
	last_name=db.Column(db.String(50))
	address1=db.Column(db.String(256))
	address2=db.Column(db.String(256))
	landmark=db.Column(db.String(256))
	state=db.Column(db.String(100))
	city=db.Column(db.String(75))
	pincode=db.Column(db.String(10))
	mobileno=db.Column(db.String(15))
	default_flag=db.Column(db.Boolean,default=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)


class Userroles(db.Model):
	
	__tablename__='userroles'
	
	role_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	role=db.Column(db.String(80),nullable=False)
	creation_date=db.Column(db.DateTime,default=datetime.datetime.utcnow())
	updation_date=db.Column(db.DateTime,onupdate=datetime.datetime.utcnow())


class Userrolesmapping(db.Model):
	__tablename__='userrolemapping'
	
	mapping_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
	user_id=db.Column(db.Integer,nullable=False)
	role_id=db.Column(db.Integer,nullable=False)



















