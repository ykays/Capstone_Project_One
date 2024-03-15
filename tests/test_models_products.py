import pytest
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, Product, ProductCategory

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield

os.environ['DATABASE_URL'] = "postgresql:///shopping-test"        

with app.app_context():
    db.create_all()

class ProductModel(TestCase):
    """Test models for product"""
    def setUp(self):
        """Setting up client and cleaning user table"""
        Product.query.delete()
        ProductCategory.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    @pytest.mark.usefixtures("app_ctx")
    def test_category_model_basic(self):
        """Basic product category model test"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()

        self.assertEqual(category.category_name, "fruits")
        self.assertEqual(category.category_details, "Apples, Bananas, etc")
    
    @pytest.mark.usefixtures("app_ctx")
    def test_category_model_invalid_name(self):
        """Basic product category model test"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            category = ProductCategory(category_name='fruits', category_details='Peaches, Bananas, etc')
            db.session.add(category)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_product_model_basic(self):
        """Basic product  model test"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()
        self.category_id = category.id

        product = Product(product_name='apples', category_id=self.category_id)
        db.session.add(product)
        db.session.commit()

        self.assertEqual(product.product_name, "apples")
        self.assertEqual(product.category_id, self.category_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_product_model_invalid_category(self):
        """Product  model test with invalid category"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()
        self.category_id = category.id

        with self.assertRaises(Exception) as context:
            product = Product(product_name='apples', category_id=999999)
            db.session.add(product)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_product_model_invalid_name(self):
        """Product  model test with invalid nae"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()
        self.category_id = category.id

        with self.assertRaises(Exception) as context:
            product = Product(None, category_id=self.category_id)
            db.session.add(product)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_product_category_relationship(self):
        """Product  model test with invalid nae"""
        category = ProductCategory(category_name='fruits', category_details='Apples, Bananas, etc')
        db.session.add(category)
        db.session.commit()
        self.category_id = category.id

        product = Product(product_name='apples', category_id=self.category_id)
        db.session.add(product)
        db.session.commit()
        self.product_id = product.id

        cat = ProductCategory.query.get(self.category_id)
        db.session.delete(cat)
        db.session.commit()

        p1 = Product.query.get(self.product_id)
        self.assertEqual(p1.product_name, "apples")
        self.assertIsNone(p1.category_id)

