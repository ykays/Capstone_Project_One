from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """A form to register new user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    location = StringField('Location')

class LoginForm(FlaskForm):
    """A form to login user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class NewTemplateForm(FlaskForm):
    """A form to add a new Grocery Template"""

    template_name = StringField('Template Name', validators=[InputRequired()])

class EditTemplateForm(FlaskForm):
    """A form to add/update products into a template""" 

    