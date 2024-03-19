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


templates_bp = Blueprint("templates", __name__)

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator


##### TEMPLATES ROUTES - View/Create/Edit/Delete Templates #####

@templates_bp.route('/templates')
@logged_in
def show_templates():
   """Main route to view/add/edit user's grocery template"""
   return render_template('templates.html')

@templates_bp.route('/api/templates')
@logged_in
def get_template():
   """To get user's grocery template, if exists"""
   user_id = functions.get_user_id(session['username'])
   users_templates = [template.serialize() for template in ListTemplate.query.filter(ListTemplate.user_id == user_id).all()]
   return jsonify(users_templates)

@templates_bp.route('/api/templates', methods=['POST'])
@logged_in
def create_template():
   """To create a new template"""
   user_id = functions.get_user_id(session['username'])
   template_name = request.json['name']
   new_template = ListTemplate(template_name=template_name, user_id = user_id)
   db.session.add(new_template)
   db.session.commit()
   return (jsonify(template=new_template.serialize()), 201)

@templates_bp.route('/api/templates/<int:id>', methods=['DELETE'])
@logged_in
def delete_template(id):
   """To delete user's template"""
   template = ListTemplate.query.get_or_404(id)
   db.session.delete(template)
   db.session.commit()
   return jsonify(message= "deleted")

@templates_bp.route('/api/templates/<int:id>')
@logged_in
def get_template_details(id):
   """To get single template details"""
   template_products =  []
   all_products = db.session.query(Product.id, Product.product_name, ProductCategory.category_name).join(TemplateProduct).join(ProductCategory).filter(TemplateProduct.template_id==id).all()
   for product in all_products:
      template_products.append(product._asdict())
   return jsonify({"data":template_products})

@templates_bp.route('/api/templates/product/<int:id>', methods=['DELETE'])
@logged_in
def delete_template_product(id):
   """To delete single product from template list"""
   user_id = functions.get_user_id(session['username'])
   template = ListTemplate.query.filter(ListTemplate.user_id == user_id).first()
   template_product = TemplateProduct.query.filter((TemplateProduct.product_id == id) & 
                                                   (TemplateProduct.template_id == template.id)).first()
   
   db.session.delete(template_product)
   db.session.commit()
   return jsonify(message= "deleted", template=template.id)

@templates_bp.route('/api/templates/product/<int:id>', methods=['POST'])
@logged_in
def add_template_product(id):
   """To add a product to a template"""
   user_id = functions.get_user_id(session['username'])
   template = ListTemplate.query.filter(ListTemplate.user_id == user_id).first()
   product_exist_check = TemplateProduct.query.filter((TemplateProduct.template_id == template.id) 
                                                      & (TemplateProduct.product_id == id)).all()
   
   if len(product_exist_check) != 0: 
        return jsonify(message="already exists", template=template.id)
   
   template_product = TemplateProduct(template_id=template.id, product_id=id)
   db.session.add(template_product)
   db.session.commit()
   return (jsonify(message="added", template=template.id),201)
   