import pytest
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc



from models import db, User, Product, ProductCategory, Reminder

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

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_model_basic(self):
        """Basic reminder model test"""
        reminder = Reminder(user_id=self.user_id, product_id=self.product_id, quantity= 2)
        db.session.add(reminder)
        db.session.commit()
        self.reminder_id = reminder.id
        
        self.assertEqual(reminder.id, self.reminder_id)
        self.assertEqual(reminder.product_id, self.product_id)
        self.assertEqual(reminder.user_id, self.user_id)
        self.assertEqual(reminder.quantity, 2)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_model_invalid_user(self):
        """The reminder model test with invalid user"""
        with self.assertRaises(Exception) as context:
            reminder = Reminder(user_id=0000, product_id=self.product_id, quantity= 2)
            db.session.add(reminder)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_model_invalid_product(self):
        """The reminder model test with invalid product"""
        with self.assertRaises(Exception) as context:
            reminder = Reminder(user_id=self.user_id, product_id=0000, quantity= 2)
            db.session.add(reminder)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_model_invalid_qty(self):
        """The reminder model test with invalid quantity"""
        with self.assertRaises(Exception) as context:
            reminder = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=None)
            db.session.add(reminder)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_user_relationship(self):
        """Testing reminder-user relationship"""
        reminder = Reminder(user_id=self.user_id, product_id=self.product_id, quantity= 2)
        db.session.add(reminder)
        db.session.commit()
        self.reminder_id = reminder.id
        
        user = User.query.get(self.user_id)
        db.session.delete(user)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            Reminder.query.get_or_404(self.reminder_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_reminder_product_relationship(self):
        """Testing reminder-product relationship"""
        reminder = Reminder(user_id=self.user_id, product_id=self.product_id, quantity= 2)
        db.session.add(reminder)
        db.session.commit()
        self.reminder_id = reminder.id
        
        product = Product.query.get(self.product_id)
        db.session.delete(product)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            Reminder.query.get_or_404(self.reminder_id)