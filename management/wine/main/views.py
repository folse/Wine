# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, g, make_response, send_file
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Wine
from inventory_excel import WineExcel

import threading

import os, time
import simplejson

def register_request(app):
    @app.before_request
    def register_g():
        # g.status_to_title=['待沟通', '待试听', '待付费', '上课中', '已结课']
        g.status_to_title_dict={None: '', 0: '待沟通', 1: '待试听', 2: '待付费', 3: '上课中', 4: '已结课'}

    @app.after_request
    def db_commit(resp):
        db.session.commit()
        return resp

def export_inventory_excel(start_date, end_date):
    wineExcel = WineExcel(start_date, end_date)
    wineExcel.export_inventory()

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('main.html')

@main.route('/export_excel', methods=['POST'])
@login_required
def export_excel():
    if request.method == 'POST':
        category = request.args.get('category', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')

        threads = []
        thread = threading.Thread(target=export_inventory_excel,args=(start_date,end_date))
        threads.append(thread)
        for t in threads:
            t.setDaemon(True)
            t.start()

        data = { "msg":"Executed", "code":"0000" }
        
        return simplejson.dumps(data)

@main.route('/get_excel_progress', methods=['GET'])
@login_required
def get_excel_progress():
    type = request.args.get('type', '')

    if type == 'inventory':
        file_name = 'inventory.log'
    elif type == 'wine':
        file_name = 'wine.log'

    if os.path.exists(file_name):
        log_file = open(file_name)
        log_msg = log_file.readline()
        data = { "msg":log_msg, "code":"0000" }
    else:
        data = { "msg":'Generating...', "code":"0000" }
    
    return simplejson.dumps(data)

@main.route('/download_excel')
@login_required
def download_excel():
    type = request.args.get('type', '')
    if type == 'inventory':
        file_name = 'inventory.xlsx'
    elif type == 'wine':
        file_name = 'wine.xlsx'
    file_path = '../' + file_name
    response = make_response(send_file(file_path))
    response.headers["Content-Disposition"] = "attachment; filename=%s;" % file_name
    return response
