import pytest
import os
from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()

class UserViewsTestCase(TestCase):
    """Test models for user"""
    def setUp(self):
        """Setting up client and cleaning user table"""
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_home_new_user(self):
        """Testing home page when the user is not in logged in"""

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please register', html)

    @pytest.mark.usefixtures("app_ctx")
    def test_home_logged_user(self):
        """Testing home page when the user is logged in"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['username'] = self.u1_username
            
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome, test_user', html)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_register_user(self):
        """Testing registering form"""
        
        with app.test_client() as client:
            data = {"username": "test_username", "password": "test_password", "email": "test@gmail.com"}
            resp = client.post('/register', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome, test_username', html)
            self.assertEqual(session['username'], "test_username")


    @pytest.mark.usefixtures("app_ctx")
    def test_register_user_invalid_username(self):
        """Testing registering form with invalid username"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            data = {"username": "test_user", "password": "password", "email": "testuser@gmail.com"}
            resp = client.post('/register', data=data)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('This username/email already exists', html)
            self.assertNotEqual(session.get("username"), "test_username")
    
    @pytest.mark.usefixtures("app_ctx")
    def test_register_user_invalid_email(self):
        """Testing registering form with invalid email"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            data = {"username": "testuser1", "password": "password", "email": "test@gmail.com"}
            resp = client.post('/register', data=data)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('This username/email already exists', html)
            self.assertNotEqual(session.get("username"), "test_username")