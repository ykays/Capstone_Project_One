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

analytics_bp = Blueprint("analytics", __name__)

def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator

##### Analytics ####
@analytics_bp.route('/analytics')
@logged_in
def history_analytics_page():
   """To display charts and history of grocery spending"""
   
   user_id = functions.get_user_id(session['username'])
   date = datetime.today() - timedelta(days=31);
   fig = analytics_functions.total_price_to_date(date, user_id)
   render_template_string(fig.to_html())
   f1 = fig.to_html()

   fig2 = analytics_functions.total_number_items_bought(user_id, date)
   render_template_string(fig2.to_html())
   f2 = fig2.to_html() 

   fig3 = analytics_functions.total_number_items_bought_vs_price_for_date(user_id, date)
   render_template_string(fig3.to_html())
   f3 = fig3.to_html()

   fig4 = analytics_functions.total_products_per_category(user_id, date)
   render_template_string(fig4.to_html())
   f4 = fig4.to_html()

   fig5 = analytics_functions.most_expensive_groceries(user_id)
   render_template_string(fig5.to_html())
   f5 = fig5.to_html()
   return render_template('analytics.html',  f1=f1, f2=f2, f3=f3, f4=f4, f5=f5 )