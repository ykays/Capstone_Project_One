import pytest
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, User

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        

with app.app_context():
    db.create_all()

class UserModelTestCase(TestCase):
    """Test models for user"""
    def setUp(self):
        """Setting up client and cleaning user table"""
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_user_model_basic(self):
        """Basic user model test"""
        user = User(username="test_user", password="test_password", email='test@gmail.com')

        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test_password")
        self.assertEqual(user.email, "test@gmail.com")

    @pytest.mark.usefixtures("app_ctx")
    def test_user_signup(self):
        """Testing user sign up class method"""

        user = User.signup("test_user", "test_password", "test@gmail.com")

        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@gmail.com")

    @pytest.mark.usefixtures("app_ctx")
    def test_user_authenticate(self):
        """Testing user authenticate class method"""
        user = User.signup("test_user", "test_password", "test@gmail.com")

        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.authenticate("test_user", "test_password"), user)

    @pytest.mark.usefixtures("app_ctx")
    def test_user_signup_invalid_username(self):
        """Testing user sign up class method with invalid username"""
        
        with self.assertRaises(Exception) as context:
            user = User.signup(None, "test_password", "test@gmail.com")
            db.session.add(user)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_user_signup_invalid_password(self):
        """Testing user sign up class method with invalid password"""
        
        with self.assertRaises(Exception) as context:
            user = User.signup("test_user", None, "test@gmail.com")
            db.session.add(user)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_user_signup_invalid_email(self):
        """Testing user sign up class method with invalid email"""
        
        with self.assertRaises(Exception) as context:
            user = User.signup("test_user", "test_password", None)
            db.session.add(user)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_user_authenticate_invalid_username(self):
        """Testing user authenticate class method with invalid username"""

        user = User.signup("test_user", "test_password", "test@gmail.com")

        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticate("testuser", "test_password"), user)

    @pytest.mark.usefixtures("app_ctx")
    def test_user_authenticate_invalid_password(self):
        """Testing user authenticate class method with invalid password"""

        user = User.signup("test_user", "test_password", "test@gmail.com")

        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticate("test_user", "testpassword"), user)
