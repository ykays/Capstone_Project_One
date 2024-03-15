from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
import requests
import dotenv
import os 
from models import db, connect_db, User, Template, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

dotenv.load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bqzupvye:3o5RMKVSuMpw09pkfhDKmH_ARQ8qMb5z@bubble.db.elephantsql.com/bqzupvye'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
# app.config['SQLALCHEMY_ECHO'] = True
#debug = DebugToolbarExtension(app)

BASE_URL = "https://api.edamam.com"
app_id = os.environ['APPLICATION_ID']
app_key = os.environ['APPLICATION_KEY']

connect_db(app)

@app.route('/')
def home():
  ####edamam
  # params = {'app_id': app_id, 'app_key': app_key, 'ingr': 'tomato', 'nutrition-type': 'logging'}
  # req1 = requests.get('https://api.edamam.com/api/food-database/v2/parser', params=params)

  # ##autocomplete
  # params = {'app_id': app_id, 'app_key': app_key, 'q': 'tomat', 'limit': '10'}
  # req2 = requests.get('https://api.edamam.com/auto-complete', params=params)


  
  # resp1 = req1.json()
  # resp2 = req2.json()

  return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  """A form to register user"""
  form = RegisterForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    location = form.location.data
    new_user = User.signup(username, password, email, location)
    
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

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    """The user will be logged out and the session will be cleared"""
    session.pop('username')
    # session.clear()
    flash("You've logged out successfully", "success")
    return redirect('/')

