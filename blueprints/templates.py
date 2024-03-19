from flask import Blueprint, Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os 
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import plotly.express as px
from datetime import datetime, date, timedelta
from functools import wraps
import services


templates_bp = Blueprint("templates", __name__)

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      user_id = services.templates.get_user_id(session['username'])
      return func(*args, user_id = user_id, **kwargs)
   return decorator


##### TEMPLATES ROUTES - View/Create/Edit/Delete Templates #####

@templates_bp.route('/templates')
@logged_in
def show_templates(user_id):
   """Main route to view/add/edit user's grocery template"""
   return render_template('templates.html')

@templates_bp.route('/api/templates')
@logged_in
def get_template(user_id):
   """To get user's grocery template, if exists"""
   users_templates = services.templates.get_user_templates(user_id)
   return jsonify(users_templates)

@templates_bp.route('/api/templates', methods=['POST'])
@logged_in
def create_template(user_id):
   """To create a new template"""
   template_name = request.json['name']
   new_template = services.templates.create_new_template(template_name, user_id)
   return (jsonify(template=new_template), 201)

@templates_bp.route('/api/templates/<int:id>', methods=['DELETE'])
@logged_in
def delete_user_template(id, user_id):
   """To delete user's template"""
   template = services.templates.delete_template(id)
   return jsonify(message= "deleted")

@templates_bp.route('/api/templates/<int:id>')
@logged_in
def get_user_template_products(id, user_id):
   """To get template products"""
   template_products = services.templates.get_template_products(id)
   return jsonify({"data":template_products})

@templates_bp.route('/api/templates/product/<int:id>', methods=['DELETE'])
@logged_in
def delete_user_template_product(id, user_id):
   """To delete single product from template list"""
   template_products = services.templates.delete_template_product(user_id, id)
   return jsonify(message= "deleted", template=template_products)

@templates_bp.route('/api/templates/product/<int:id>', methods=['POST'])
@logged_in
def add_user_template_product(id, user_id):
   """To add a product to a template"""
   add_product = services.templates.add_template_product(user_id, id)
   return add_product
   