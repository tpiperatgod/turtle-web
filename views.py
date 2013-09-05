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


@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    info = '[*] IAASAPI POWER ON [*]'
    return render_template('index.html', info=info)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST', 'DELETE'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist['file']
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
    return render_template('upload_pic.html')



