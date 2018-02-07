from flask import Blueprint, render_template, url_for, redirect, flash, request
from models import ProductMaster


product_management = Blueprint('product_management', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')
# from .extensions import db
