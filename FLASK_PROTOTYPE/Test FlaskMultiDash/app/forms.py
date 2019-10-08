from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    role = SelectField('Select Role', validators=[DataRequired()], choices=[('doctor','Doctors'), ('researcher','Researchers')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    role = SelectField('Select Role', validators=[DataRequired()], choices=[('doctor','Doctors'), ('researcher','Researchers')])
    submit = SubmitField('Register')
