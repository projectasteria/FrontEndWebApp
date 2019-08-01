# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    username = StringField('Username:', validators=[validators.required(), validators.Length(min=1, max=30)])
    password = StringField('Password:', validators=[validators.required(), validators.Length(min=1, max=30)])
    email = EmailField('Email address', [validators.optional(), validators.Email()])
