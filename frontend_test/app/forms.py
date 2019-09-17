from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup, escape

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AdminForm(FlaskForm):
    username = StringField('Enter your username:')
    doctors = BooleanField('Doctor')
    researchers = BooleanField('Researcher')
    submit = SubmitField('Request')
    
