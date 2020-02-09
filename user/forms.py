from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError

from user.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
    ])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
    ])

    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
    ])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
    ])

    confirmed = PasswordField('Confirmed Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField('Register')

    def validate_username(form, field):
        if User.objects.filter(username=field.data).first():
            raise ValidationError('Username already exist')