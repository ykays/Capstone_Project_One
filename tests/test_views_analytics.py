import pytest
import os
from unittest import TestCase
from flask import session, jsonify
from models import db, connect_db, User, ListTemplate, TemplateProduct, ProductCategory, Product, GroceryList, GroceryListProducts, Reminder
import requests

os.environ['DATABASE'] = "postgresql:///shopping-test"
from app import app

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

     
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()

class TemplatesViewTestCase(TestCase):
    """Test models for user"""
    def setUp(self):
        """Setting up client and cleaning user table"""

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_analytics_main_page_invalid_user(self):
        """Testing main page of analytics with no user"""

        with app.test_client() as client:
            resp = client.get('/analytics', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in to see the content', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_analytics_main_page_no_groceries(self):
        """Testing main page of analytics with user logged in but no total price"""
        lists = GroceryListProducts.query.all()
        for list in lists:
            db.session.delete(list)
        db.session.commit()

        self.username = "test_user" 
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.get('/analytics', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('The total price and checked flag need to be updated for at least one grocery list/product', response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_analytics_main_page(self):
        """Testing main page of analytics with user logged in"""
        file = open(r'seed.py', 'r').read()
        exec(file)

        self.username = "test_user" 
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.get('/analytics')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Analytics', response_data)
           