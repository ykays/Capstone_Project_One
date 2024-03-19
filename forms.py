from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField
from wtforms.validators import InputRequired, Email, Length
import email_validator

class RegisterForm(FlaskForm):
    """A form to register new user"""

    username = StringField('Username', validators=[InputRequired(), Length(min=6, message='Username needs to have at least 6 characters')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Username needs to have at least 8 characters')])
    email = StringField('Email', validators=[InputRequired(), Email()])

class LoginForm(FlaskForm):
    """A form to login user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



    