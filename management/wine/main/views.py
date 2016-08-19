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
        g.info_status_to_title_dict={None: '', 0: '待确认', 1: '有效', 2: '无效', 3: '已试听'}

    @app.after_request
    def db_commit(resp):
        db.session.commit()
        return resp

@login_required
@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/admin/wine')

# @main.route('/wines', methods=['GET'])
# @login_required
# def wines():
#     form=WineForm()
#     page=request.args.get('page', 1, type=int)
#     pagination=Wine.query.order_by(Wine.created_at.desc()).paginate(
#         page, per_page=current_app.config['CUSTOMERS_PER_PAGE'],
#         error_out=False)
#     wines=pagination.items

#     return render_template('main.html', form=form, wines=wines, pagination=pagination)


# @main.route('/wine/<int:id>', methods=['GET', 'POST'])
# @login_required
# def wine(id):
#     wine=Wine.query.get_or_404(id)
#     form=WineForm()
#     form.name.data=wine.name
#     return render_template('wine.html', form=form)
            