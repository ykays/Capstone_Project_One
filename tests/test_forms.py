from flask import Flask
from unittest import TestCase
from models import User
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
            form = RegisterForm()
            form.username.data= "test_user"
            form.password.data= "test_password"
            form.email.data = "test@gmail.com"
            print(form.username)
            form.validate()
            print(form.validate())
            print(form.errors)
            assert form.validate_on_submit() is True
                
