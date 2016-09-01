# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, g
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Wine


def register_request(app):
    @app.before_request
    def register_g():
        # g.status_to_title=['待沟通', '待试听', '待付费', '上课中', '已结课']
        g.status_to_title_dict={None: '', 0: '待沟通', 1: '待试听', 2: '待付费', 3: '上课中', 4: '已结课'}

    @app.after_request
    def db_commit(resp):
        db.session.commit()
        return resp

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    permission=False
    for role in current_user.roles:
        if role.name == 'admin':
            permission=True
            pass
    return render_template('main.html', permission=permission)

@main.route('/export_excel', methods=['POST'])
@login_required
def export_excel():
    permission=False
    for role in current_user.roles:
        if role.name == 'admin':
            permission=True
            pass
    if request.method == 'POST':
        category = request.args.get('category', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        print category
        print start_date
        print end_date
    return render_template('main.html', permission=permission)

