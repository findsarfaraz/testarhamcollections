from extensions import db

class Testset(db.Model):
	id =db.Column(db.Integer,primary_key=True,autoincrement=True)
	name=db.Column(db.String(80))

	def __init__(self, name):
		self.name = name