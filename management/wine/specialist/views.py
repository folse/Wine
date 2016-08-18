# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, g
from flask.ext.login import login_required, current_user
from .forms import SpecialistForm

from . import specialist

from .. import db
from ..models import User

@specialist.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def specialist(id):
    user = User.query.get_or_404(id)
    form = SpecialistForm()
    if form.validate_on_submit():
        user.realname = form.realname.data
        user.mobile = form.mobile.data
        db.session.add(user)
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('main.index'))
    else :
        form.realname.data = user.realname
        form.mobile.data = user.mobile
        return render_template('specialist/specialist.html', form=form)
