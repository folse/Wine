from . import admin
from flask import redirect
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView as _ModelView
from .models import *

class ModelView(_ModelView):

    column_display_pk = True

    def is_accessible(self):

        if current_user.is_anonymous:
            return False

    	for role in current_user.roles:
        	if role.name == 'admin':
        		return True
        return False

    def inaccessible_callback(self, name):
        return redirect('/auth/login')

class UserAdmin(ModelView):
    can_delete = False
    column_searchable_list = ['id', 'username', 'email']
    column_exclude_list = ['password']

class WineAdmin(ModelView):
    list_template = 'admin/list.html'
    can_create = False
    can_delete = False
    can_edit = False
    column_searchable_list = ['id', 'name', 'number']
    column_exclude_list = ['id', 'sys_wine_id', 'status', 'url', 'fragrance', 'color', 'sugar', 'ingredient', 'created_at', 'updated_at']

class StoreAdmin(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_searchable_list = ['id', 'name', 'city', 'sys_store_id']
    column_exclude_list = ['created_at', 'updated_at']

class InventoryAdmin(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_searchable_list = ['id', 'inventory','wine_id', 'wine_name', 'wine_number', 'store_id']
    column_exclude_list = ['id', 'created_at']

class RoleAdmin(ModelView):
    column_searchable_list = ['id', 'name']

# admin.add_view(UserAdmin(User, db.session))
admin.add_view(WineAdmin(Wine, db.session))
admin.add_view(StoreAdmin(Store, db.session))
admin.add_view(InventoryAdmin(Inventory, db.session))
# admin.add_view(RoleAdmin(Role, db.session))