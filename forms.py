from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    username = StringField('username',[InputRequired()])
    email = StringField('Email address',[InputRequired()])
    password = PasswordField('password',[EqualTo('password_confirmation',message='Passwords Must Match')])
    password_confirmation = PasswordField('Confirm Password',validators=[Length(min = 8, max = 25)])

    def validate_username(self,username_to_check):
        from models import User
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This Username is already exists, try a different username !')
    def validate_email(self,email_to_check):
        from models import User
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('This email is already exists, try a different email !')


class LoginForm(FlaskForm):
    username = StringField('Username',[InputRequired()])
    password = PasswordField('Password',[InputRequired()])

class ProductForm(FlaskForm):
    name = StringField('Product Name',[InputRequired()])
    item_photo = StringField('Product Picture',[InputRequired])
    description = StringField('Description',[InputRequired()])
