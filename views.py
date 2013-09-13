#!/usr/bin/env python
#*-*coding:utf-8*-*
#
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Blueprint, abort, jsonify
from flaskext import uploads
from flask.views import MethodView
from werkzeug import secure_filename
from app import app
from db import dbapi
from utils import baseutils


@app.before_request
def before_request():
    pass

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
    if request.method == 'POST':
        pwd = request.form.get('password', None)
        if pwd:
            new_pwd = baseutils.hash_password(pwd)
            print new_pwd
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
        if pwd:
            new_pwd = baseutils.hash_password(pwd)
            print new_pwd
        user_info = dbapi.user_get_by_email(e)
        print user_info
        if new_pwd == user_info['password']:
            print "True"
            flash("hello %s" % user_info['email'])
            return redirect(url_for('index'))


