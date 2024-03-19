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
        User.query.delete()
        ListTemplate.query.delete()
        TemplateProduct.query.delete()
        Product.query.delete()
        ProductCategory.query.delete()
        GroceryList.query.delete()
        GroceryListProducts.query.delete()
        Reminder.query.delete()
        

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

        template = ListTemplate(template_name ="test_user_template", user_id = self.user_id)
        db.session.add(template)
        db.session.commit()
        self.template_id = template.id
        
        tp1 = TemplateProduct(template_id=self.template_id, product_id=self.product_id)
        db.session.add(tp1)
        db.session.commit()
        self.tp_id = tp1.id


        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    @pytest.mark.usefixtures("app_ctx")
    def test_lists_main_page_invalid_user(self):
        """Testing grocery lists main page user not logged in"""

        with app.test_client() as client:
            resp = client.get('/lists', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in to see the content', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_lists_main_page(self):
        """Testing grocery lists main page"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username
            resp = client.get('/lists')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('View/Add/Update Grocery List', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_creating_grocery_list_invalid_user(self):
        """Testing creating new grocery list when user is not logged in"""

        with app.test_client() as client:
            date = '2024-09-27'
            resp = client.get(f'/api/list/products/{date}', follow_redirects=True)
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in to see the content', response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_creating_grocery_list(self):
        """Testing creating new grocery list for a new date"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            date = '2024-09-27'
            resp = client.get(f'/api/list/products/{date}')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn('"date": "Fri, 27 Sep 2024', response_data)
            self.assertIn('apples', response_data)
           
    @pytest.mark.usefixtures("app_ctx")
    def test_retrieving_grocery_list(self):
        """Testing retrieving new grocery list for an existing date"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.get(f'/api/list/products/{self.grocery_date}')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('"date": "Fri, 15 Mar 2024', response_data)
            self.assertIn('apples', response_data)
            self.assertIn('2', response_data)
            self.assertIn('"category_name": "Fruits"', response_data)
           
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_grocery_list_no_template(self):
        """Testing creatting new grocery list when the template does not exist"""

        template = ListTemplate.query.get_or_404(self.template_id)
        db.session.delete(template)
        db.session.commit()

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            date = '2024-09-28'
            resp = client.get(f'/api/list/products/{date}')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Template needed', response_data)

    @pytest.mark.usefixtures("app_ctx")
    def test_adding_product_to_grocery_list(self):
        """Testing adding new product to grocery list"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.post('/api/list/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date, "product_id": self.product_id,
                                        "quantity": 5});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn(str(self.product_id), response_data)
            self.assertIn(str(self.grocery_list_id), response_data)
            self.assertIn('5', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_product_to_grocery_list_invalid_user(self):
        """Testing adding new product to grocery list invalid user"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        with app.test_client() as client:

            resp = client.post('/api/list/products',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date, "product_id": self.product_id,
                                        "quantity": 5}, follow_redirects=True);
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in to see the content', response_data)

 
    @pytest.mark.usefixtures("app_ctx")
    def test_deleting_product_from_list(self):
        """Testing deleting product from the list"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.delete(f'/api/list/products/{self.glp_id}')
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('deleted', response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_updating_list_product(self):
        """Testing updating the list product"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.patch(f'/api/list/products/{self.glp_id}',  
                               headers={'Content-Type': 'application/json'},
                               json = {"quantity": 5, "bought": True});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn(str(self.grocery_list_id), response_data)
            self.assertIn(str(self.product_id), response_data)
            self.assertIn('"bought": true', response_data)
            self.assertIn(str(5), response_data)
           
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_reminders_to_list_update(self):
        """Testing adding reminders to the list when the product already existed"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        r1 = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=10)
        db.session.add(r1)
        db.session.commit()
        self.r_id = r1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.post(f'/api/list/products/reminders',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn("The reminders have been added", response_data)

            r = Reminder.query.get(self.r_id)
            self.assertIsNone(r)

            glp = GroceryListProducts.query.get(self.glp_id)
            self.assertEqual(10, glp.quantity)

    @pytest.mark.usefixtures("app_ctx")
    def test_adding_reminders_to_list_with_no_reminders(self):
        """Testing adding reminders to the list"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.post(f'/api/list/products/reminders',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("No reminders have been found", response_data)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_adding_reminders_to_list_add(self):
        """Testing adding reminders to the list when the product didn't exist"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date


        r1 = Reminder(user_id=self.user_id, product_id=self.product_id, quantity=10)
        db.session.add(r1)
        db.session.commit()
        self.r_id = r1.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.post(f'/api/list/products/reminders',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date});
            
            response_data = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 201)
            self.assertIn("The reminders have been added", response_data)

            r = Reminder.query.get(self.r_id)
            self.assertIsNone(r)

            glp = GroceryListProducts.query.filter(GroceryListProducts.product_id == self.product_id, 
                                                   GroceryListProducts.grocery_list_id == self.grocery_list_id).all()
            
            self.assertEqual(len(glp), 1)
            self.assertEqual([10], [prod.quantity for prod in glp])
            self.assertEqual([self.product_id], [prod.product_id for prod in glp])

    @pytest.mark.usefixtures("app_ctx")
    def test_update_list_price(self):
        """Testing updating price"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.patch('/api/list',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date, "price": 150.89});
            
            response_data = resp.get_data(as_text=True)

            list = GroceryList.query.get(self.grocery_list_id)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The price has been updated", response_data)
            self.assertEqual(150.89, list.total_price)
    
    @pytest.mark.usefixtures("app_ctx")
    def test_update_list_price_with_blank(self):
        """Testing updating price with blank"""

        gl1 = GroceryList(user_id=self.user_id, date='2024-03-15', template_id=self.template_id)
        db.session.add(gl1)
        db.session.commit()
        self.grocery_list_id = gl1.id
        self.grocery_date = gl1.date

        glp = GroceryListProducts(grocery_list_id=self.grocery_list_id, product_id=self.product_id, quantity=2)
        db.session.add(glp)
        db.session.commit()
        self.glp_id = glp.id

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = self.username

            resp = client.patch('/api/list',  
                               headers={'Content-Type': 'application/json'},
                               json = {"date": self.grocery_date, "price":''});
            
            response_data = resp.get_data(as_text=True)

            list = GroceryList.query.get(self.grocery_list_id)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The price has been updated", response_data)
            self.assertEqual(0, list.total_price)