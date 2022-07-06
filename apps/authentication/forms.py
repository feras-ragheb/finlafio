# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, TextField,PasswordField,SelectMultipleField,SelectField)
from wtforms.validators import Email, DataRequired ,InputRequired

# login and registration


class LoginForm(FlaskForm):
    username = TextField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

    plan = SelectField(choices=(
                (1, 'Free'),
                (2, 'PAID'),
            ),validators=[DataRequired()], coerce=int)
    favorite_news = SelectMultipleField(choices=(
                (1, 'BBC'),
                (2, 'CNN'),
                (3, 'Aljazeera'),
            ),validators=[DataRequired()], coerce=int)
    favorite_stocks = SelectMultipleField(choices=(
                (1, 'APP'),
                (2, 'Google'),
            ),validators=[DataRequired()], coerce=int)

    favorite_influancer = SelectMultipleField(choices=(
                (1, 'Elyon Mask'),
                (2, 'Jeff Bezos'),
            ),validators=[DataRequired()], coerce=int)        

    
    
    
