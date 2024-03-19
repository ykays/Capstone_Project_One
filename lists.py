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


lists_bp = Blueprint("lists", __name__)

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator

#### LISTS ROUTES ####

@lists_bp.route('/lists')
@logged_in
def show_lists_page():
   """To show all lists where the user can add/edit/delete them"""
   return render_template('lists.html')

@lists_bp.route('/api/list/products/<date>')
@logged_in
def get_list_products(date):
   """To get all products of the user's grocery list"""
   check_list_exists = functions.check_grocery_list_exist(session["username"], date)
   if check_list_exists:
      list_id = functions.get_user_grocery_list_id(session['username'], date)
      list_products = functions.get_all_products_list(list_id, date)
      return jsonify(list=list_products)
   
   check_template_exists = functions.get_user_template_id(session["username"])
   if not check_template_exists:
      return jsonify(message='Template needed')

   new_list = functions.add_new_grocery_list(session["username"], date)
   return (jsonify(list=new_list), 201)
      

@lists_bp.route('/api/list/products', methods=['POST'])
@logged_in
def add_new_product_to_list():
   """To add a new product to grocery list"""
   date = request.json['date']
   list_id = functions.get_user_grocery_list_id(session['username'], date)
   new_glp = GroceryListProducts(grocery_list_id=list_id, product_id=request.json['product_id'], quantity=request.json['quantity'])
   db.session.add(new_glp)
   db.session.commit()
   return (jsonify(product=new_glp.serialize()), 201)

@lists_bp.route('/api/list/products/<int:id>', methods=['DELETE'])
@logged_in
def delete_product(id):
   """To delete a product from the grocery list"""
   list_product = GroceryListProducts.query.get_or_404(id)
   db.session.delete(list_product)
   db.session.commit()
   return jsonify(message='deleted') 

@lists_bp.route('/api/list/products/<int:id>', methods=["PATCH"])
@logged_in
def update_quantity_product(id):
   """To update quantity of item from don't forget list"""
   list_product = GroceryListProducts.query.get_or_404(id)
   list_product.quantity = request.json.get('quantity', list_product.quantity)
   list_product.bought = request.json.get('bought', list_product.bought)
   db.session.commit()
   return (jsonify(list_product=list_product.serialize()), 201)

@lists_bp.route('/api/list/products/reminders', methods=['POST'])
@logged_in
def add_reminders_to_the_list():
   """To update the grocery list with saved reminders. Once the list is updated the reminders are deleted"""
   date = request.json['date']
   reminders = functions.compare_reminders_with_current_list(session['username'], date)
   if reminders == False:
      return jsonify(message="No reminders have been found")
   return (jsonify(message="The reminders have been added"),201)

@lists_bp.route('/api/list', methods=['PATCH'])
@logged_in
def update_grocery_list():
   """To update grocery list"""
   user_id = functions.get_user_id(session['username'])
   date = request.json['date']
   price = request.json['price']
   
   grocery_list = GroceryList.query.filter(GroceryList.user_id == user_id, GroceryList.date==date).first()
   grocery_list.total_price = 0 if price == '' else price
   
   db.session.commit()
   return jsonify(message="The price has been updated") 
