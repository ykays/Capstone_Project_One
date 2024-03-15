import pytest
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from datetime import datetime


from models import db, User, ListTemplate, Product, ProductCategory, GroceryList, GroceryListProducts

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        

with app.app_context():
    db.create_all()

class Template(TestCase):
    """Test models for product"""
    def setUp(self):
        """Setting up client, cleaning user table, adding sample data"""
        with app.app_context():
             db.drop_all()
             db.create_all()
        
        user = User(username="test_user", password="test_password", email='test@gmail.com')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()
        self.category_id = category.id

        product = Product(product_name='apples', category_id=self.category_id)
        db.session.add(product)
        db.session.commit()
        self.product_id = product.id

        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_model_basic(self):
        """Basic grocery list model test"""
        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id
        
        self.assertEqual(grocery_list.id, self.grocery_list_id)
        self.assertEqual(grocery_list.user_id, self.user_id)
        self.assertEqual(grocery_list.template_id, self.template_id)
      
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_invalid_user(self):
        """The grocery list model test with invalid user"""
        with self.assertRaises(Exception) as context:
            grocery_list = GroceryList(user_id=0000, date=datetime.now(), template_id=self.template_id)
            db.session.add(grocery_list)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_invalid_date(self):
        """The grocery list model test with date"""
        with self.assertRaises(Exception) as context:
            grocery_list = GroceryList(user_id=self.user_id, date=None, template_id=self.template_id)
            db.session.add(grocery_list)
            db.session.commit()
      
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_full_model(self):
        """Full grocery list model test"""
        grocery_list = GroceryList(
            user_id=self.user_id, 
            date=datetime.now(),
            template_id=self.template_id,
            total_price=35.56)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id
        
        self.assertEqual(grocery_list.id, self.grocery_list_id)
        self.assertEqual(grocery_list.user_id, self.user_id)
        self.assertEqual(grocery_list.template_id, self.template_id)
        self.assertEqual(grocery_list.total_price, 35.56) 

    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_product_model(self):
        """Testing grocery list product model"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        grocery_list_product = GroceryListProducts(
            grocery_list_id=self.grocery_list_id, 
            product_id=self.product_id,
            quantity=1)
        db.session.add(grocery_list_product)
        db.session.commit()
        self.grocery_list_product_id = grocery_list_product.id
        
        self.assertEqual(grocery_list_product.id, self.grocery_list_product_id)
        self.assertEqual(grocery_list_product.product_id, self.product_id)
        self.assertEqual(grocery_list_product.quantity, 1)
        self.assertEqual(grocery_list_product.bought, False)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_product_model_invalid_grocery_list(self):
        """Testing grocery list product model with invalid grocery list"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        with self.assertRaises(Exception) as context:
            grocery_list_product = GroceryListProducts(
                grocery_list_id=0000, 
                product_id=self.product_id,
                quantity=1)
            db.session.add(grocery_list_product)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_product_model_invalid_product(self):
        """Testing grocery list product model with invalid product"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        with self.assertRaises(Exception) as context:
            grocery_list_product = GroceryListProducts(
                grocery_list_id=self.grocery_list_id, 
                product_id=00000,
                quantity=1)
            db.session.add(grocery_list_product)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_product_model_invalid_quantity(self):
        """Testing grocery list product model with invalid product"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        with self.assertRaises(Exception) as context:
            grocery_list_product = GroceryListProducts(
                grocery_list_id=self.grocery_list_id, 
                product_id=self.product_id,
                quantity='str')
            db.session.add(grocery_list_product)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_product_model_relationship(self):
        """Testing grocery list product with grocery list relationship"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        grocery_list_product = GroceryListProducts(
            grocery_list_id=self.grocery_list_id, 
            product_id=self.product_id,
            quantity=1)
        db.session.add(grocery_list_product)
        db.session.commit()
        self.grocery_list_product_id = grocery_list_product.id

        gl = GroceryList.query.get(self.grocery_list_id)
        db.session.delete(gl)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            GroceryListProducts.query.get_or_404(self.grocery_list_product_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_grocery_list_user_relationship(self):
        """Testing grocery list with user relationship"""

        grocery_list = GroceryList(user_id=self.user_id, date=datetime.now(), template_id=self.template_id)
        db.session.add(grocery_list)
        db.session.commit()
        self.grocery_list_id = grocery_list.id

        user = User.query.get(self.user_id)
        db.session.delete(user)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            GroceryList.query.get_or_404(self.grocery_list_id)