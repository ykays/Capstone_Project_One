from flask import Flask
from unittest import TestCase
# from wtforms_test import FormTestCase
# from flask_wtf import FlaskForm
from app import app
from forms import RegisterForm
import pytest
from app import app
from forms import RegisterForm, LoginForm

app.config['WTF_CSRF_ENABLED']=False  


class UserFormTestCase(TestCase):


    def test_register_form(self):
        """Testing register user form"""
        
        with app.test_request_context(method="POST"):

            # user = {"username": "test_user", "password": "test_password", "email": "test@gmail.com"}
            form = RegisterForm(username="test_user", password="test_password", email="test@gmail.com")
            # form.username.data= "test_user"
            # form.data['password'] = "test_password"
            # form.data['email'] = "test@gmail.com"
            # user = User(form.username.data, form.email.data,
            #     form.password.data)
            # if form.validate_on_submit():
            #     form.username.data = "test_user"
            #     form.password.data = "test_password"
            #     form.email.data = "test@gmail.com"
            
            form.validate()
            print(form.validate())
            print((form.errors))
            self.assertTrue(form.validate())
                
