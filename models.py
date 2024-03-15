from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    location = db.Column(db.Text)

    templates = db.relationship('Template', cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', cascade="all, delete-orphan")
    grocery_lists = db.relationship('GroceryList', cascade="all, delete-orphan")

    @classmethod
    def signup(cls, username, password, email,location=None ):
        """Class method to Sign up user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        return cls(username=username, password=hashed_pwd, email=email, location=location)
    
    @classmethod
    def authenticate(cls, username, password):
        """Class method to authenticate users to login"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    
class Template(db.Model):
    """Grocery Template Model"""

    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_name = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    template_products = db.relationship('TemplateProduct', cascade="all, delete-orphan")
    grocery_lists = db.relationship('GroceryList') 

class ProductCategory(db.Model):
    """Product Category Model"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.Text, nullable=False, unique=True)
    category_details = db.Column(db.Text, nullable=False)

    products = db.relationship('Product') 

class Product(db.Model):
    """Product Model"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    reminders = db.relationship('Reminder', cascade="all, delete-orphan")
    template_products = db.relationship('TemplateProduct', cascade="all, delete-orphan")
    grocery_list_products = db.relationship('GroceryListProducts',cascade="all, delete-orphan")
    
class TemplateProduct(db.Model):
    """Template-Product relationship Model"""

    __tablename__ = 'template_product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

class Reminder(db.Model):
    """Remember to Buy List Model"""

    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class GroceryList(db.Model):
    """Grocery List Model"""

    __tablename__ = 'grocery_lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    completed = db.Column(db.Boolean, nullable=False, default=False)
    total_price = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
 
    grocery_list_products = db.relationship('GroceryListProducts', cascade="all, delete-orphan")
 
class GroceryListProducts(db.Model):
    """Grocery List Products Relationship Model"""

    __tablename__ = 'grocery_list_products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grocery_list_id = db.Column(db.Integer, db.ForeignKey('grocery_lists.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    bought = db.Column(db.Boolean, nullable=False, default=False)

   

