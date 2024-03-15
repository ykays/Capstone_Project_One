import pytest
import os
from unittest import TestCase
from app import app
from flask import session, jsonify
from models import db, connect_db, User, ListTemplate, TemplateProduct, ProductCategory, Product, GroceryList, GroceryListProducts
import requests

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()

class TemplatesViewTestCase(TestCase):
    """Test models for user"""
    def setUp(self):
        """Setting up client and cleaning user table"""
        User.query.delete()
        ListTemplate.query.delete()
        TemplateProduct.query.delete()
        Product.query.delete()
        ProductCategory.query.delete()
        GroceryList.query.delete()
        GroceryListProducts.query.delete()
        

        test_user = User.signup(username = "test_user" , password="testuserpassword" , email="testuser@gmail.com")
        
        db.session.add(test_user)
        db.session.commit()
        
        self.username = test_user.username
        self.user_id = test_user.id

        category = ProductCategory(category_name='Fruits', category_details="Apples, Bananas, etc")
        db.session.add(category)
        db.session.commit()
        self.category_name = category.category_name
        self.category_id = category.id
        
        product = Product(product_name='apples', category_id=self.category_id)
        db.session.add(product)
        db.session.commit()
        self.product_name = product.product_name
        self.product_id = product.id

        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id
        
        tp1 = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp1)
        db.session.commit()
        self.tp_id = tp1.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    # @pytest.mark.usefixtures("app_ctx")
    # def test_retrieve_products(self):
    #     """Testing getting list of products"""

    #     with app.test_client() as client:
    #         resp = client.get('/api/products')
    #         response_data = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('apples', response_data)
    #         self.assertIn('Fruits', response_data)