from flask import Blueprint, Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os 
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import functions
import analytics_functions
import plotly.express as px
from datetime import datetime, date, timedelta
from functools import wraps


external_search_bp = Blueprint("external_search", __name__)

dotenv.load_dotenv()

BASE_URL = "https://api.edamam.com"
app_id = os.environ['APPLICATION_ID']
app_key = os.environ['APPLICATION_KEY']

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator

@external_search_bp.route('/external_search')
@logged_in
def externach_search_page():
   """Page with external API search for a product"""
   return render_template('external_search.html')

@external_search_bp.route('/search/external/<name>')
@logged_in
def search_via_external_api(name):
   params = {'app_id': app_id, 'app_key': app_key, 'ingr': name, 'nutrition-type': 'logging'}
   request = requests.get('https://api.edamam.com/api/food-database/v2/parser', params=params)
   response = request.json()
   return jsonify(response)
   
@external_search_bp.route('/api/categories')
@logged_in
def get_all_product_categories():
   """To get a list of all available product categories"""
   categories = [category.serialize() for category in ProductCategory.query.all()]
   return jsonify(categories)

@external_search_bp.route('/api/products', methods=['POST'])
@logged_in
def adding_new_product():
   """To add a new product"""
   product_name = request.json['product']
   category_id=request.json['category_id']
   find_product =  Product.query.filter(Product.product_name == product_name, Product.category_id==category_id).all()
   if len(find_product) != 0:
      return (jsonify(message='already exists'))

   new_product = Product(product_name=product_name, category_id=category_id)
   db.session.add(new_product)
   db.session.commit()
   return (jsonify(product=new_product.serialize()), 201)
