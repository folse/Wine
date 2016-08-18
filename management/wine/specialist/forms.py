# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpecialistForm(Form):
    realname = StringField('姓名', validators=[Required(), Length(0, 64)])
    mobile = StringField('手机号', validators=[Required(), Length(11,11,'请输入11位的手机号')])
    submit = SubmitField('保存')
