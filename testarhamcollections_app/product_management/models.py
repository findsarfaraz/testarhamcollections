from ..extensions import db
import datetime


class ProductMaster(db.Model):
    __tablename__ = 'productmaster'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_title = db.Column(db.String(1000))
    creation_date = db.Column(db.Datetime, default=datetime.datetime.utcnow())
    updation_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    is_live = db.Column(db.Boolean, default=False)
