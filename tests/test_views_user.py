import pytest
from unittest import TestCase
from flask import session
from models import db, connect_db, User
import os

os.environ['DATABASE'] = "postgresql:///shopping-test"
from app import app

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield


# os.environ['DATABASE'] = "postgresql://shopping-test"
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.create_all()


class UserViewsTestCase(TestCase):
    """Test models for user"""

    def setUp(self):
        """Setting up client and cleaning user table"""
        # os.environ['DATABASE'] = "postgresql:///shopping-test"
        User.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE']

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
    def test_register_user_page(self):
        """Testing registering form page"""

        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register to Easy Grocery App!', html)

    @pytest.mark.usefixtures("app_ctx")
    def test_register_user(self):
        """Testing registering form"""

        with app.test_client() as client:
            data = {"username": "test_username",
                    "password": "test_password", "email": "test@gmail.com"}
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
            data = {"username": "test_user", "password": "password",
                    "email": "testuser@gmail.com"}
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
            data = {"username": "testuser1",
                    "password": "password", "email": "test@gmail.com"}
            resp = client.post('/register', data=data)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('This username/email already exists', html)
            self.assertNotEqual(session.get("username"), "test_username")

    @pytest.mark.usefixtures("app_ctx")
    def test_login_page(self):
        """Testing login form page"""

        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Log In to Easy Grocery App!', html)

    @pytest.mark.usefixtures("app_ctx")
    def test_login_user(self):
        """Testing login form"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            data = {"username": "test_user", "password": "test_password"}
            resp = client.post('/login', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome, test_user!', html)
            self.assertEqual(session['username'], "test_user")

    @pytest.mark.usefixtures("app_ctx")
    def test_login_user_invalid_username(self):
        """Testing login form with invalid username"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            data = {"username": "testuser", "password": "test_password"}
            resp = client.post('/login', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid Username/Password', html)
            self.assertIsNone(session.get('username'))

    @pytest.mark.usefixtures("app_ctx")
    def test_login_user_invalid_password(self):
        """Testing login form with invalid password"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.u1_username = u1.username

        with app.test_client() as client:
            data = {"username": "test_user", "password": "testpassword"}
            resp = client.post('/login', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid Username/Password', html)
            self.assertIsNone(session.get('username'))

    @pytest.mark.usefixtures("app_ctx")
    def test_logout_user(self):
        """Testing logout"""
        u1 = User.signup("test_user", "test_password", "test@gmail.com")
        db.session.add(u1)
        db.session.commit()
        self.username = u1.username

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("logged out successfully", html)
