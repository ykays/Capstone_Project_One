import pytest
import os
from unittest import TestCase
from app import app
from flask import session, jsonify
from models import db, connect_db, User, ListTemplate, TemplateProduct, ProductCategory, Product

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
    def test_templates_user_not_logged_in(self):
        """Testing templates page when the user is not logged in"""

        with app.test_client() as client:
            resp = client.get('/templates', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in to see the content', html)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_templates_user_logged_in(self):
        """Testing templates page when the user is logged in"""
        
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['username'] = self.username
        
            resp = client.get('/templates')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a new template', html)
            self.assertIn('<h2>My Template - Add/Remove product</h2>', html)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_templates_getting_user_template(self):
        """Testing templates page when the user is logged in & has a template"""

        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
        
            resp = client.get('/api/templates')
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_user_template', resp_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_templates_getting_user_template_when_it_does_not_exist(self):
        """Testing templates page when the user is logged in & doesn't have a template"""
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
        
            resp = client.get('/api/templates')
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("[]", resp_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_new_template(self):
        """Testing creating new template"""
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.post('/api/templates',  
                               headers={'Content-Type': 'application/json'},
                               json = {"name": "test_template"});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn("test_template", resp_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_deleting_template(self):
        """Testing deleting template"""
        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.delete(f'/api/templates/{self.template_id}',  
                               headers={'Content-Type': 'application/json'});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("deleted", resp_data)
    
    
    @pytest.mark.usefixtures("app_ctx")
    def test_template_details(self):
        """Testing getting template details"""
        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name
        
        tp1 = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp1)
        db.session.commit()

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.get(f'/api/templates/{self.template_id}',  
                               headers={'Content-Type': 'application/json'});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("apples", resp_data)


    @pytest.mark.usefixtures("app_ctx")
    def test_delete_template_details(self):
        """Testing deleting template item"""
        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name
        
        tp1 = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp1)
        db.session.commit()
        self.tp_id = tp1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.delete(f'/api/templates/product/{self.product_id}',  
                               headers={'Content-Type': 'application/json'});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("deleted", resp_data)
            self.assertIn(str(self.template_id), resp_data)

    
    @pytest.mark.usefixtures("app_ctx")
    def test_add_template_product(self):
        """Testing adding template product"""
        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.post(f'/api/templates/product/{self.product_id}',  
                               headers={'Content-Type': 'application/json'});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn("added", resp_data)
            self.assertIn(str(self.template_id), resp_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_add_template_product_that_exists(self):
        """Testing adding template product that already exists in the list"""

        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()

        self.template_id = template.id
        self.template_name = template.template_name
        
        tp1 = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp1)
        db.session.commit()
        self.tp_id = tp1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            
            resp = client.post(f'/api/templates/product/{self.product_id}',  
                               headers={'Content-Type': 'application/json'});
           
            resp_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("already exists", resp_data)
            self.assertIn(str(self.template_id), resp_data)
   
    

            
    
    