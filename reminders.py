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


reminders_bp = Blueprint("reminders", __name__)

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator

######## Reminders routes ######
@reminders_bp.route('/reminders')
@logged_in
def show_reminders_page():
   """To show all don't forget items where the user can add/edit/delete them"""
   return render_template('reminders.html')

@reminders_bp.route('/api/reminders/products', methods=['POST'])
@logged_in
def add_reminder_product():
   """To add a product to user's don't forget list"""
   user_id = functions.get_user_id(session['username'])
   new_reminder = Reminder(user_id=user_id, product_id=request.json['product_id'], quantity=request.json.get('quantity'))
   db.session.add(new_reminder)
   db.session.commit()
   return (jsonify(reminder=new_reminder.serialize()), 201)

@reminders_bp.route('/api/reminders/products')
@logged_in
def get_reminders_for_user():
   """To retrieve user's don't forget items"""
   user = User.query.filter(User.username == session['username']).first()
   reminders = []
   all_reminders = db.session.query(Product.id, Product.product_name, ProductCategory.category_name, Reminder.id, Reminder.user_id, Reminder.product_id, Reminder.quantity).join(Reminder).join(ProductCategory).filter(Reminder.user_id == user.id).all()
   for reminder in all_reminders:
      reminders.append(reminder._asdict())
   return jsonify({"data":reminders})

@reminders_bp.route('/api/reminders/products/<int:id>', methods=['DELETE'])
@logged_in
def delete_product_from_reminder_list(id):
   """To delete product from user's don't forget list"""
   reminder = Reminder.query.get_or_404(id)
   db.session.delete(reminder)
   db.session.commit()
   return jsonify(message='deleted')

@reminders_bp.route('/api/remiders/products', methods=["PATCH"])
@logged_in
def update_quantity_reminder():
   """To update quantity of item from don't forget list"""
   reminder = Reminder.query.get_or_404(request.json['id'])
   reminder.quantity = request.json['quantity']
   db.session.commit()
   return (jsonify(reminder=reminder.serialize()), 201)
