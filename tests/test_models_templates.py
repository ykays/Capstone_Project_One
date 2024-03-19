import pytest
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, ListTemplate, Product, ProductCategory, TemplateProduct

os.environ['DATABASE'] = "postgresql:///shopping-test"
from app import app

@pytest.fixture
def app_ctx():
    with app.app_context():
        yield
   

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
    def test_template_model_basic(self):
        """Basic template model test"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        
        self.assertEqual(template.template_name, "test_template")
        self.assertEqual(template.user_id, self.user_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_model_invalid_template_name(self):
        """List template model test with invalid template name"""
        with self.assertRaises(Exception) as context:
            template = ListTemplate(None, user_id=self.user_id)
            db.session.add(template)
            db.session.commit()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_model_invalid_user_id(self):
        """List template model test with invalid user id"""
        with self.assertRaises(Exception) as context:
            template = ListTemplate(template_name='test_template', user_id=000000)
            db.session.add(template)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_template_product_model_basic(self):
        """Basic template model test"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        tp = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp)
        db.session.commit()
        
        self.assertEqual(tp.template_id, self.template_id)
        self.assertEqual(tp.product_id, self.product_id) 
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_product_model_invalid_template(self):
        """Template Product model test with invalid template"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        with self.assertRaises(Exception) as context:
            tp = TemplateProduct(template_id=00000, product_id=self.product_id)
            db.session.add(tp)
            db.session.commit()

    @pytest.mark.usefixtures("app_ctx")
    def test_template_product_model_invalid_user(self):
        """Template Product model test with invalid user"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        with self.assertRaises(Exception) as context:
            tp = TemplateProduct(self.template_id, product_id=00000)
            db.session.add(tp)
            db.session.commit()
        
    @pytest.mark.usefixtures("app_ctx")
    def test_template_product_template_relationship(self):
        """Testing relationship between Template and Template Product"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        tp = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp)
        db.session.commit()
        self.tp_id= tp.id

        lt = ListTemplate.query.get(self.template_id)
        db.session.delete(lt)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            TemplateProduct.query.get_or_404(self.tp_id)
    
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_user_relationship(self):
        """Testing relationship between Template and User"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        user = User.query.get(self.user_id)
        db.session.delete(user)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            ListTemplate.query.get_or_404(self.template_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_user_relationship_with_template_products(self):
        """Testing relationship between Template and User"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        tp = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp)
        db.session.commit()
        self.tp_id= tp.id

        user = User.query.get(self.user_id)
        db.session.delete(user)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            TemplateProduct.query.get_or_404(self.tp_id)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_products_relationship_with_products(self):
        """Testing relationship between Template Products and Products"""
        template = ListTemplate(template_name='test_template', user_id=self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id

        tp = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp)
        db.session.commit()
        self.tp_id= tp.id

        product = Product.query.get(self.product_id)
        db.session.delete(product)
        db.session.commit()

        with self.assertRaises(Exception) as context:
            TemplateProduct.query.get_or_404(self.tp_id)


