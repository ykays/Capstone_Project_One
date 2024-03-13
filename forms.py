from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """A form to register new user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

class LoginForm(FlaskForm):
    """A form to login user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



    