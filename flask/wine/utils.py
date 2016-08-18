# -*- coding:utf-8 -*-
from .models import User, Role

def is_admin(user_or_user_id):
    if isinstance(user_or_user_id, User):
        user = user_or_user_id
    else:
        user = User.query.get(user_or_user_id)
    for role in user.roles:
        if role.name == 'admin':
            return True
    return False

