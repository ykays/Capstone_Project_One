import pytest
import os
from unittest import TestCase
from app import app
from flask import session, jsonify
from models import db, connect_db, User, ListTemplate, TemplateProduct, ProductCategory, Product
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

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_retrieve_products(self):
        """Testing getting list of products"""

        with app.test_client() as client:
            resp = client.get('/api/products')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('apples', response_data)
            self.assertIn('Fruits', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_retrieve_categories(self):
        """Testing getting list of categories"""

        with app.test_client() as client:
            resp = client.get('/api/categories')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fruits', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_external_search_user_not_logged_in(self):
        """Testing external search when user is not logged in"""

        with app.test_client() as client:
            resp = client.get('/external_search', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You need to be logged in to use this search', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_external_search_user_logged_in(self):
        """Testing external search when user is  logged in"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
        
            resp = client.get('/external_search')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Find a Product, Assign a Category & Add to Easy Grocery Database', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_new_product_user_not_logged_in(self):
        """Testing adding new products when user is  logged in"""
        with app.test_client() as client:
        
            resp = client.post('/api/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"product": "Sweet Corn", "category_id": 2});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('access unauthorized', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_new_product_user_logged_in(self):
        """Testing adding new products when user is  logged in"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
        
            resp = client.post('/api/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"product": "Sweet Corn", "category_id": self.category_id});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn('Sweet Corn', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_new_product_that_exists(self):
        """Testing adding new product that already exists"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
        
            resp = client.post('/api/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"product": "apples", "category_id": self.category_id});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('already exists', response_data)

    

  