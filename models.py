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
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)

    templates = db.relationship('ListTemplate', cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', cascade="all, delete-orphan")
    grocery_lists = db.relationship('GroceryList', cascade="all, delete-orphan")

    @classmethod
    def signup(cls, username, password, email):
        """Class method to Sign up user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        return cls(username=username, password=hashed_pwd, email=email)
    
    @classmethod
    def authenticate(cls, username, password):
        """Class method to authenticate users to login"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    
class ListTemplate(db.Model):
    """Grocery Template Model"""

    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    template_name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    template_products = db.relationship('TemplateProduct', cascade="all, delete-orphan")
    grocery_lists = db.relationship('GroceryList') 

    def serialize(self):
            return {
        'id': self.id,
        'template_name': self.template_name,
        'user_id': self.user_id
    } 
class ProductCategory(db.Model):
    """Product Category Model"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(80), nullable=False, unique=True)
    category_details = db.Column(db.Text, nullable=False)


    def serialize(self):
            return {
        'id': self.id,
        'category_name': self.category_name,
        'category_details': self.category_details
    } 

    product = db.relationship('Product')

class Product(db.Model):
    """Product Model"""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    reminders = db.relationship('Reminder', cascade="all, delete-orphan")
    template_products = db.relationship('TemplateProduct', cascade="all, delete-orphan")
    grocery_list_products = db.relationship('GroceryListProducts',cascade="all, delete-orphan")
    

    def serialize(self):
            return {
        'id': self.id,
        'product_name': self.product_name,
        'category_id': self.category_id
    } 

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
    quantity = db.Column(db.Integer, nullable=False, default=1)

    
    
    def serialize(self):
            return {
        'id': self.id,
        'user_id': self.user_id,
        'product_id': self.product_id,
        'quantity': self.quantity
    } 
class GroceryList(db.Model):
    """Grocery List Model"""

    __tablename__ = 'grocery_lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    total_price = db.Column(db.Float)

 
    grocery_list_products = db.relationship('GroceryListProducts', cascade="all, delete-orphan")
    
class GroceryListProducts(db.Model):
    """Grocery List Products Relationship Model"""

    __tablename__ = 'grocery_list_products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grocery_list_id = db.Column(db.Integer, db.ForeignKey('grocery_lists.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    bought = db.Column(db.Boolean, nullable=False, default=False)

    def serialize(self):
            return {
        'id': self.id,
        'grocery_list_id': self.grocery_list_id,
        'product_id': self.product_id,
        'quantity': self.quantity,
        'bought': self.bought,
    }

