from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=50)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=6, max=80)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=50)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=6, max=80)]
    )
    invite_key = StringField(
        "Invite Key", validators=[InputRequired(), Length(min=10, max=10)]
    )
    role = SelectField(
        "Select Role",
        validators=[DataRequired()],
        choices=[("doctor", "Doctor"), ("researcher", "Researcher")],
    )
    submit = SubmitField("Register")


class KeyGenForm(FlaskForm):
    role = SelectField(
        "Select Role",
        validators=[DataRequired()],
        choices=[("doctor", "Doctor"), ("researcher", "Researcher")],
    )
    submit = SubmitField("Generate Invite Key")
