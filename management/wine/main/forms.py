# -*- coding:utf-8 -*-
from flask import request
from flask_wtf import Form
from wtforms.fields.html5 import TelField
from wtforms import StringField, TextAreaField, BooleanField, SelectField, RadioField, FieldList, FormField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CustomerForm(Form):
    name = StringField('姓名', validators=[Length(0, 64)])