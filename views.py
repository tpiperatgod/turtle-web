#!/usr/bin/env python
#*-*coding:utf-8*-*
#coding=utf-8
import os, sys
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Blueprint, abort, jsonify
from flask.views import MethodView
from werkzeug import secure_filename
from app import app
from db import dbapi, db_init, session
from utils import baseutils

@app.before_request
def before_request():
    g.user = None
#     g.site = dbapi.site_get(1)
#     if 'user_id' in session:
#         g.user = query_db('select * from ep_user where user_id = %s', 
#                           session['user_id'], one=True)

@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    pass
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST', 'DELETE'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
    return render_template('upload_pic.html')

@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    error = None
    if request.method == 'POST':
        checkemail = dbapi.user_get_by_email(request.form.get('email'))
        if not checkemail.get('id', None):
            error = "此邮箱已被注册，请使用新的邮箱。"
            return render_template('index.html', error=error)
        pwd = request.form.get('password', None)
        pwd_rp = request.form.get('passwordRp', None)
        if pwd == pwd_rp:
            new_pwd = baseutils.hash_password(pwd)
            print new_pwd
        else:
            error = "两次输入的密码不同，请重新确认！"
            return render_template('index.html', error=error)

        sign_info = {"email": request.form.get('email', None),
                     'name': request.form.get('name', 'default'),
                     'password': new_pwd}
        dbapi.user_create(sign_info)
    return redirect(url_for('index'))

@app.route('/user_signin', methods=['GET', 'POST'])
def user_signin():
    if request.method == 'POST':
        pwd = request.form.get('password', None)
        e = request.form.get('email', None)
        if e and pwd:
            new_pwd = baseutils.hash_password(pwd)
            print new_pwd
            user_info = dbapi.user_get_by_email(e)
        else:
            error = "需要输入Email。"
            return render_template('index.html', error=error)
        
        print user_info
        if new_pwd == user_info['password']:
            print "True"
            flash("hello %s" % user_info['email'])
            session['user_id'] = user_info['id']
            return redirect(url_for('index'))
        else:
            error = "密码有误！"
            return render_template('index.html', error=error)

@app.route('/topic', methods=['GET', 'POST'])
def topic_index():
    pass
    return render_template('topic_index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_index():
    if request == 'POST':
        site_info = {'name': request.args.get('site_name', None),
                     'title': request.args.get('public_title', None),
                     'description': request.args.get('public_description', None)}
        
        for k,v in site_info:
            if not v:
                del site_info[k]
        print site_info
        dbapi.site_update(1, site_info)
    return render_template('admin_index.html')

@app.route('/init_db')
def init_db():
    _ENGINE = session.get_engine()
    db_init.upgrade(_ENGINE)
    default_site_info = {'name': '海龟终结者',
                         'title': '海龟终结者的独白',
                         'description': 'long long ago'}
    dbapi.site_create(default_site_info)
    return redirect(url_for('index'))