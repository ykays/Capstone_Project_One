from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
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
from templates import templates_bp
from lists import lists_bp
from reminders import reminders_bp
from analytics import analytics_bp
from external_search import external_search_bp


dotenv.load_dotenv()

app = Flask(__name__)
app.register_blueprint(templates_bp)
app.register_blueprint(lists_bp)
app.register_blueprint(reminders_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(external_search_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

connect_db(app)

# Adding decorator to check if the user is logged in
def logged_in(func):
   @wraps(func)
   def decorator(*args, **kwargs):
      if not session.get('username'):
         flash("Please log in to see the content", "danger")
         return redirect('/')
      return func(*args, **kwargs)
   return decorator


##### REGISTER & LOGIN USER ROUTES #####

@app.route('/')
def home():
  """Home page"""
  return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  """A form to register user"""
  form = RegisterForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    new_user = User.signup(username, password, email)
    
    db.session.add(new_user)        
    try:
        db.session.commit()
    except IntegrityError:
        flash('This username/email already exists', "danger")
        return render_template('register.html', form=form)

    session['username'] = new_user.username  
    flash('You have been registered', "success")
    return redirect('/')

  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
   """A form to login user"""

   form = LoginForm()

   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = User.authenticate(username, password)

      if user:
         session['username'] = user.username
         return redirect('/')
      else:
         form.username.errors = ['Invalid Username/Password']

   return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """The user will be logged out and the session will be cleared"""
    session.pop('username')
    session.clear()
    flash("You've logged out successfully", "success")
    return redirect('/')

#### API Products route (used by all routes) ###
@app.route('/api/products')
@logged_in
def get_all_products():
   """To get the list of all products"""

   prod_list= []
   products = db.session.query(Product.id, Product.product_name, Product.category_id, ProductCategory.category_name).join(ProductCategory).all()
   
   for product in products:
      prod_list.append(product._asdict())

   return jsonify(prod_list)