from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for
import requests
import dotenv
import os 
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import functions

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
app.app_context().__enter__()

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
    flash("You've logged out successfully", "success")
    return redirect('/')

@app.route('/templates')
def show_templates():
   """Main route to view/add/edit user's grocery template"""
   return render_template('templates.html')

@app.route('/api/templates')
def get_template():
   """To get user's grocery template, if exists"""
   user = User.query.filter(User.username == session['username']).first()
   users_templates = [template.serialize() for template in ListTemplate.query.filter(ListTemplate.user_id == user.id).all()]
   return jsonify(users_templates)

@app.route('/api/templates', methods=['POST'])
def create_template():
   """To create a new template"""
   user = User.query.filter(User.username == session['username']).first()
   new_template = ListTemplate(template_name=request.json['name'], user_id = user.id)
   db.session.add(new_template)
   db.session.commit()
   return (jsonify(template=new_template.serialize()), 201)

@app.route('/api/templates/<int:id>', methods=['DELETE'])
def delete_template(id):
   """To delete user's template"""
   template = ListTemplate.query.get_or_404(id)
   db.session.delete(template)
   db.session.commit()
   
   return jsonify(message= "deleted")

@app.route('/api/templates/<int:id>')
def get_template_details(id):
   """To get single template details"""
   temp_products =  []
   all_products = db.session.query(Product.id, Product.product_name, ProductCategory.category_name).join(TemplateProduct).join(ProductCategory).filter(TemplateProduct.template_id==id).all()
   for product in all_products:
      temp_products.append(product._asdict())
   return jsonify({"data":temp_products})

@app.route('/api/templates/product/<int:id>', methods=['DELETE'])
def delete_template_product(id):
   """To delete single product from template list"""
   user = User.query.filter(User.username == session['username']).first()
   template = ListTemplate.query.filter(ListTemplate.user_id == user.id).first()
   template_product = TemplateProduct.query.filter((TemplateProduct.product_id == id) & 
                                                   (TemplateProduct.template_id == template.id) ).first()
   db.session.delete(template_product)
   db.session.commit()
   
   return jsonify(message= "deleted", template=template.id)

@app.route('/api/templates/product/<int:id>', methods=['POST'])
def add_template_product(id):
   """To add a product to a template"""
   user = User.query.filter(User.username == session['username']).first()
   template = ListTemplate.query.filter(ListTemplate.user_id == user.id).first()
   product_exist_check = TemplateProduct.query.filter((TemplateProduct.template_id == template.id) 
                                                      & (TemplateProduct.product_id == id)).all()
   
   if product_exist_check: 
        return jsonify(message="already exists")
   
   template_product = TemplateProduct(template_id=template.id, product_id=id)
   db.session.add(template_product)
   db.session.commit()
   return jsonify(message="added", template=template.id)
   


@app.route('/api/products')
def get_all_products():
   """To get the list of all products"""

   prod_list= []
   products = db.session.query(Product.id, Product.product_name, Product.category_id, ProductCategory.category_name).join(ProductCategory).all()
   
   for product in products:
      prod_list.append(product._asdict())

   return jsonify(prod_list)


