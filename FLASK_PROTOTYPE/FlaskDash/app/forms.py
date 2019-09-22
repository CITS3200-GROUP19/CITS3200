from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired()])
#     password = PasswordField('Password', validators=[InputRequired()])
#     submit = SubmitField('Register')
