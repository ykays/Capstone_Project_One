import pytest
import os
from unittest import TestCase
from app import app
from flask import session, jsonify
from models import db, connect_db, User, ProductCategory, Product, Reminder
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
    def test_reminders_home_page_no_user(self):
        """Testing reminders page when the user is not logged in"""

        with app.test_client() as client:
            resp = client.get('/reminders', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You need to be logged in to add/view", response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_reminders_home_page_user_logged(self):
        """Testing reminders page when the user is logged in"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            resp = client.get('/reminders')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("-forget-List", response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_adding_reminder(self):
        """Testing adding new don't forget item"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.post('/api/reminders/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"product_id": self.product_id, "quantity": 2});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn(str(self.product_id), response_data)
            self.assertIn(str(2), response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_reminder_invalid_user(self):
        """Testing adding new don't forget item when user is not logged in"""

        with app.test_client() as client:

            resp = client.post('/api/reminders/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"product_id": self.product_id, "quantity": 2});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("access unauthorized", response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_get_reminders(self):
        """Testing retrieving reminders"""
        r1 = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=3)
        db.session.add(r1)
        db.session.commit()

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            resp = client.get('/api/reminders/products')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(str(self.product_id), response_data)
            self.assertIn(str(self.product_name), response_data)
            self.assertIn(str(3), response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_deleting_reminders(self):
        """Testing deleting reminders"""
        r1 = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=3)
        db.session.add(r1)
        db.session.commit()
        self.r_id = r1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            resp = client.delete(f'/api/reminders/products/{self.r_id}')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("deleted", response_data)
   
    @pytest.mark.usefixtures("app_ctx")
    def test_updating_reminder(self):
        """Testing updating reminder"""
        r1 = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=3)
        db.session.add(r1)
        db.session.commit()
        self.r_id = r1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.patch('/api/remiders/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"id": self.r_id, "quantity": 5});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn(str(5), response_data)