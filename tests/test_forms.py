import os
from flask import Flask
from unittest import TestCase
from models import User
from forms import RegisterForm, LoginForm

os.environ['DATABASE'] = "postgresql:///shopping-test"
from app import app

app.config['WTF_CSRF_ENABLED']=False  


class UserFormTestCase(TestCase):
         
    def test_register_form(self):
        """Testing register user form"""
        
        with app.test_request_context(method="POST"):

            form = RegisterForm()
            form.username.data= "test_user"
            form.password.data= "test_password"
            form.email.data = "test@gmail.com"

            assert "username" in form.data
            assert "password" in form.data
            assert "email" in form.data
    
    def test_registration_form_validation_is_working(self):
         self.app = app.test_client()
         with self.app as client:

            form = {
                 "username": "test_user",
                 "password": "test_password",
                 "email": "test@gmail.com"
            }
        
            response = client.post('/register', data=form, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
    
    def test_login_form_validation_is_working(self):
         self.app = app.test_client()
         with self.app as client:

            form = {
                 "username": "test_user",
                 "password": "test_password",
            }
        
            response = client.post('/login', data=form, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
              
    def test_login_form(self):
     """Testing login user form"""
        
    with app.test_request_context(method="POST"):

            form = LoginForm()
            form.username.data= "test_user"
            form.password.data= "test_password"
           

            assert "username" in form.data
            assert "password" in form.data

    def test_registration_form_doesnt_include_unexpected_fields(self):
            
            with app.test_request_context():
                form = RegisterForm()
                form.username.data = 'sample-username'
                form.password.data = 'sample-password'
                form.email.data = 'sample-email'

                keys = list(form.data.keys())

                keys.remove('username')
                keys.remove('password')
                keys.remove('email')

                assert keys == [
                ], f"Unexpected fields found in the RegisterForm: {', '.join(keys)}"

    def test_login_form_doesnt_include_unexpected_fields(self):
            
            with app.test_request_context():
                form = LoginForm()
                form.username.data = 'sample-username'
                form.password.data = 'sample-password'

                keys = list(form.data.keys())

                keys.remove('username')
                keys.remove('password')
                
                assert keys == [
                ], f"Unexpected fields found in the LoginForm: {', '.join(keys)}"


 
   
         

                
