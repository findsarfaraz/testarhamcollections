from ..extensions import db
import datetime
from flask import Flask, jsonify


#
# class CategoryMaster(db.Model):
#     __tablename__ = categorymaster

#     category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     category_name = db.Column(db.String(512), blank=False, Null=False)
#     creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#     updation_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     subcategory = db.relationship("SubCategory", backref="categorymaster", lazy=True)


# class SubCategory(db.Model):
#     __tablename__ = subcategorymaster

#     subcategory_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     subcategory_name = db.Column(db.String(512), blank=False, Null=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('categorymaster.category_id'), nullable=False)
#     creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
#     updation_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ProductMaster(db.Model):
    __tablename__ = 'productmaster'

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_title = db.Column(db.String(1000))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updation_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    is_live = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    soldoff_flag = db.Column(db.Boolean, default=False)
    cost_price = db.Column(db.Integer)
    price = db.Column(db.Integer)


class ProductImageMapping(db.Model):
    __tablename__ = 'productimagemapping'

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column(db.String(200))
    image_path = db.Column(db.String(512))
    main_image = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updation_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('productmaster.product_id'), nullable=False)


# class ProductDetail(db.Model):
#     __tablename__ = 'productdetail'
#     product_detail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product_master.product_id'), nullable=False)


class VoteTest(db.Model):
    __tablename__ = 'votetest'
    voteid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    votenumber = db.Column(db.Integer)
