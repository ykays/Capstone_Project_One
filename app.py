from flask import Flask, request, render_template, redirect, flash, session, jsonify, url_for, render_template_string
import requests
import dotenv
import os 
from models import db, connect_db, User, ListTemplate, ProductCategory, Product, TemplateProduct, Reminder, GroceryList, GroceryListProducts
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
import functions
import analytics
import plotly.express as px
from datetime import datetime, date, timedelta



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

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    """The user will be logged out and the session will be cleared"""
    session.pop('username')
    flash("You've logged out successfully", "success")
    return redirect('/')

@app.route('/templates')
def show_templates():
   """Main route to view/add/edit user's grocery template"""
   if not session.get('username'):
      flash("You need to be logged in to view/add templates", "danger")
      return redirect('/')
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

@app.route('/external_search')
def externach_search_page():
   """Page with external API search for a product"""
   if not session.get('username'):
      flash("You need to be logged in to use this search", "danger")
      return redirect('/')
   return render_template('external_search.html')

@app.route('/search/external/<name>')
def search_via_external_api(name):
   params = {'app_id': app_id, 'app_key': app_key, 'ingr': name, 'nutrition-type': 'logging'}
   request = requests.get('https://api.edamam.com/api/food-database/v2/parser', params=params)
   response = request.json()
   return jsonify(response)
   
@app.route('/categories')
def get_all_product_categories():
   """To get a list of all available product categories"""
   categories = [category.serialize() for category in ProductCategory.query.all()]
   return jsonify(categories)

@app.route('/api/products', methods=['POST'])
def adding_new_product():
   """To add a new product"""
   if not session.get('username'):
      flash("Access unauthorized.", "danger")
      return jsonify(message='access unauthorized')
   
   product_name = request.json['product']
   category_id=request.json['category_id']
   find_product =  Product.query.filter(Product.product_name == product_name, Product.category_id==category_id).all()
   if len(find_product) != 0:
      flash("This product & category already exists")
      return (jsonify(message='already exists'))

   new_product = Product(product_name=product_name, category_id=category_id)
   db.session.add(new_product)
   db.session.commit()
   return (jsonify(product=new_product.serialize()), 201)


######## Reminders routes ######
@app.route('/reminders')
def show_reminders_page():
   """To show all don't forget items where the user can add/edit/delete them"""
   if not session.get('username'):
      flash("You need to be logged in to add/view Don't forget lists", "danger")
      return redirect('/')

   return render_template('reminders.html')

@app.route('/api/reminders/products', methods=['POST'])
def add_reminder_product():
   """To add a product to user's don't forget list"""
   if  not session['username']:
      flash("Access unauthorized.", "danger")
      return jsonify(message='access unauthorized')
   
   user = User.query.filter(User.username == session['username']).first()
   new_reminder = Reminder(user_id=user.id, product_id=request.json['product_id'], quantity=request.json.get('quantity'))
   db.session.add(new_reminder)
   db.session.commit()
   return (jsonify(reminder=new_reminder.serialize()), 201)

@app.route('/api/reminders/products')
def get_reminders_for_user():
   """To retrieve user's don't forget items"""
   user = User.query.filter(User.username == session['username']).first()
   reminders = []
   all_reminders = db.session.query(Product.id, Product.product_name, ProductCategory.category_name, Reminder.id, Reminder.user_id, Reminder.product_id, Reminder.quantity).join(Reminder).join(ProductCategory).filter(Reminder.user_id == user.id).all()
   for reminder in all_reminders:
      reminders.append(reminder._asdict())
   return jsonify({"data":reminders})

@app.route('/api/reminders/products/<int:id>', methods=['DELETE'])
def delete_product_from_reminder_list(id):
   """To delete product from user's don't forget list"""
   reminder = Reminder.query.get_or_404(id)
   db.session.delete(reminder)
   db.session.commit()
   return jsonify(message='deleted')

@app.route('/api/remiders/products', methods=["PATCH"])
def update_quantity_reminder():
   """To update quantity of item from don't forget list"""
   reminder = Reminder.query.get_or_404(request.json['id'])
   reminder.quantity = request.json['quantity']
   db.session.commit()
   return (jsonify(reminder=reminder.serialize()), 201)

#### LISTS ROUTES ####

@app.route('/lists')
def show_lists_page():
   """To show all lists where the user can add/edit/delete them"""
    
   if not session.get('username'):
      flash("You need to be logged in to view/add a new list", "danger")
      return redirect('/')

   return render_template('lists.html')

@app.route('/api/list/products/<date>')
def get_list_products(date):
   """To get all products of the user's grocery list"""

   if not session.get('username'):
    return jsonify(message="You need to be logged in to view list")
  
   check_list_exists = functions.check_grocery_list_exist(session["username"], date)
   if check_list_exists:
      list_id = functions.get_user_grocery_list_id(session['username'], date)
      list_products = functions.get_all_products_list(list_id, date)
      return jsonify(list=list_products)
  
   else:
        new_list = functions.add_new_grocery_list(session["username"], date)
        return (jsonify(list=new_list), 201)
      

@app.route('/api/list/products', methods=['POST'])
def add_new_product_to_list():
   """To add a new product to grocery list"""
   if not session.get('username'):
    return jsonify(message="You need to be logged in to add a new product")
   date = request.json['date']
   list_id = functions.get_user_grocery_list_id(session['username'], date)
   new_glp = GroceryListProducts(grocery_list_id=list_id, product_id=request.json['product_id'], quantity=request.json['quantity'])
   db.session.add(new_glp)
   db.session.commit()
   return (jsonify(product=new_glp.serialize()), 201)

@app.route('/api/list/products/<int:id>', methods=['DELETE'])
def delete_product(id):
   """To delete a product from the grocery list"""
   list_product = GroceryListProducts.query.get_or_404(id)
   db.session.delete(list_product)
   db.session.commit()
   return jsonify(message='deleted') 

@app.route('/api/list/products/<int:id>', methods=["PATCH"])
def update_quantity_product(id):
   """To update quantity of item from don't forget list"""
   list_product = GroceryListProducts.query.get_or_404(id)
   list_product.quantity = request.json.get('quantity', list_product.quantity)
   list_product.bought = request.json.get('bought', list_product.bought)
   db.session.commit()
   return (jsonify(list_product=list_product.serialize()), 201)

@app.route('/api/list/products/reminders', methods=['POST'])
def add_reminders_to_the_list():
   """To update the grocery list with saved reminders. Once the list is updated the reminders are deleted"""
   date = request.json['date']
   reminders = functions.compare_reminders_with_current_list(session['username'], date)
   if reminders == False:
      return jsonify(message="No reminders have been found")
   return (jsonify(message="The reminders have been added"),201)

@app.route('/api/list', methods=['PATCH'])
def update_grocery_list():
   """To update grocery list"""
   user_id = functions.get_user_id(session['username'])
   date = request.json['date']
   price = request.json['price']
   grocery_list = GroceryList.query.filter(GroceryList.user_id == user_id, GroceryList.date==date).first()
   grocery_list.total_price = price
   grocery_list.completed=True
   db.session.commit()
   return jsonify(message="The price has been updated") 

##### Analytics ####
@app.route('/analytics')
def history_analytics_page():
   """To display charts and history of grocery spending"""
   user_id = functions.get_user_id(session['username'])
   date = datetime.today() - timedelta(days=31);
   fig = analytics.total_price_to_date(date, user_id)
   render_template_string(fig.to_html())
   x = fig.to_html()

   fig2 = analytics.total_number_items_bought(user_id, date)
   render_template_string(fig2.to_html())
   x2 = fig2.to_html() 

   fig3 = analytics.total_number_items_bought_vs_price_for_date(user_id, date)
   render_template_string(fig3.to_html())
   x3 = fig3.to_html()

   fig4 = analytics.total_products_per_category(user_id, date)
   render_template_string(fig4.to_html())
   x4 = fig4.to_html()

   fig5 = analytics.most_expensive_groceries(user_id)
   render_template_string(fig5.to_html())
   x5 = fig5.to_html()
   return render_template('analytics.html',  x=x, x2=x2, x3=x3, x4=x4, x5=x5 )