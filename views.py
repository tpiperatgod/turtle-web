#!/usr/bin/env python
#*-*coding:utf-8*-*
#coding=utf-8
import os, sys
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Blueprint, abort, jsonify, send_from_directory
from urlparse import urlparse, urljoin
from flask.views import MethodView
from werkzeug import secure_filename
from app import app
from db import dbapi, db_init
from db import session as db_session
from utils import baseutils
import time
import sae.storage

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = request.args['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = dbapi.user_get(session['user_id'])

    try:
        g.site = dbapi.site_get(1)['name']
        print g.site
    except:
        g.stie = "海龟终结者"

@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    pass
    return render_template('index.html')

@app.route('/gallery_horizon/', methods=['POST', 'GET'])
@app.route('/gallery_horizon/<int:catalog_id>/', methods=['POST', 'GET'])
def gallery_horizon(catalog_id=None):
    catalogs = dbapi.catalog_get_all()
    if catalog_id:
        s_catalog = dbapi.catalog_get_by_id(catalog_id)
        try:
            pics = dbapi.upload_get_by_catalog_id(catalog_id)
        except:
            pics = None
    else:
        s_catalog = None
        try:
            pics = dbapi.upload_get_all()
        except:
            pics = None
    return render_template('gallery_horizon.html', pics=pics, catalogs=catalogs, s_catalog=s_catalog)

@app.route('/gallery/del/', methods=['POST', 'GET'])
@app.route('/gallery/del/<int:catalog_id>/', methods=['GET', 'POST'])
def gallery_del(catalog_id=None):
    if not g.user:
        abort(401)
            
    page_func = "delete"
    catalogs = dbapi.catalog_get_all()
    if catalog_id:
        s_catalog = dbapi.catalog_get_by_id(catalog_id)
        try:
            pics = dbapi.upload_get_by_catalog_id(catalog_id)
        except:
            pics = None
    else:
        s_catalog = None
        try:
            pics = dbapi.upload_get_all()
        except:
            pics = None
    
    if request.method == 'POST':  
        upload_file_info = request.form.getlist('up_file', None)
        if upload_file_info:
            s = sae.storage.Client() 
            for file_id in upload_file_info:
                filename = dbapi.upload_get(file_id)['name']
                dbapi.uoload_destroy(file_id)
                s.delete(app.config['DOMAIN_NAME'], filename)
            return redirect(url_for('gallery_del', catalog_id=catalog_id))
    return render_template('gallery_manage.html', pics=pics, catalogs=catalogs,
                            s_catalog=s_catalog, page_func=page_func)
    
@app.route('/gallery/edit/', methods=['POST', 'GET'])
@app.route('/gallery/edit/<int:catalog_id>/', methods=['GET', 'POST'])
def gallery_edit(catalog_id=None):
    if not g.user:
        abort(401)

    page_func = "edit"
    catalogs = dbapi.catalog_get_all()
    if catalog_id:
        s_catalog = dbapi.catalog_get_by_id(catalog_id)
        try:
            pics = dbapi.upload_get_by_catalog_id(catalog_id)
        except:
            pics = None
    else:
        s_catalog = None
        try:
            pics = dbapi.upload_get_all()
        except:
            pics = None
    
    if request.method == 'POST':  
        pics_info = request.form.getlist('up_file', None)
        i = 0
        session['upload_cache'] = {}
        for pic_id in pics_info:
            i += 1
            pic_filename = dbapi.upload_get(pic_id)['name']
            pic_url = dbapi.upload_get(pic_id)['url']
            session['upload_cache'][i] = {'upload_id': pic_id,
                                          'upload_name': pic_filename,
                                          'upload_url': pic_url}
            print session['upload_cache']
            return redirect(url_for('pre_public'))
    return render_template('gallery_manage.html', pics=pics, catalogs=catalogs,
                            s_catalog=s_catalog, page_func=page_func)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if not g.user:
        abort(401)

    if request.method == 'POST':
        files = request.files.getlist('file')
        i = 0
        session['upload_cache'] = {}
        for file in files:
            if file and allowed_file(file.filename):
                i += 1
                filename_s = secure_filename(file.filename)
                exetensions = filename_s.split('.')[-1]
                filenmae_n = str(time.time()) + str(i) + '.' + exetensions

                s = sae.storage.Client()  
                ob = sae.storage.Object(file.read())  
                url = s.put(app.config['DOMAIN_NAME'], filenmae_n, ob)

                upload_info = {'user': 1,
                               'name': filenmae_n,
                               'url': url,
                               'heat': 0,
                               'types': exetensions}
                dbapi.upload_create(upload_info)
                n_data = dbapi.upload_get_by_url(url)
                session['upload_cache'][i] = {'upload_id': n_data['id'],
                                              'upload_name': filenmae_n,
                                              'upload_url': url}
        return redirect(url_for('pre_public'))
    return render_template('upload.html')

@app.route('/upload/pre_public/', methods=['GET', 'POST'])
def pre_public():
    if not g.user:
        abort(401)

    uploads = session['upload_cache']

    if not uploads:
        abort(404)
        
    for e in uploads:
        upload_description = dbapi.upload_get(uploads[e]['upload_id'])['description']
        upload_catalog = dbapi.upload_get(uploads[e]['upload_id'])['catalog']
        uploads[e]['upload_description'] = upload_description
        uploads[e]['upload_catalog'] = upload_catalog
        
    catalogs = dbapi.catalog_get_all()

    if request.method == 'POST':
        upload_update = {}
        for i in uploads:
            upload_update = {'catalog': request.form.get('pic_catalog' + str(i), None),
                             'description': request.form.get('pic_description' + str(i), None)}
            print upload_update
            dbapi.upload_update(uploads[i]['upload_id'], upload_update)
            session['upload_cache'] = None
        return redirect(url_for('gallery_horizon'))
    return render_template('pic_edit.html', uploads=uploads, catalogs=catalogs)

#@app.route('/upload/<filename>/')
#def uploaded_file(filename):
#    return send_from_directory(app.config['DOMAIN_NAME'],
#                               filename)
#    s = sae.storage.Client() 
#    print s.url(app.config['DOMAIN_NAME'], filename)
#    print s.stat(app.config['DOMAIN_NAME'], filename)
#    return send_from_directory(app.config['DOMAIN_NAME'], filename)

@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
    if not g.user:
        abort(401)

    next = get_redirect_target()
    if request.method == 'POST':
        catalog_info = {'name': request.form.get('catalogname', None)}
        dbapi.catalog_create(catalog_info)
        return redirect_back('index')
    return render_template('catalog.html')

@app.route('/catalog/del/', methods=['GET', 'POST'])
def catalog_del():
    if not g.user:
        abort(401)

    if request.method == 'POST':
        catalog_info = request.form.getlist('catalog', None)
        if catalog_info:
            for catalog in catalog_info:
                dbapi.catalog_destroy(catalog)
                upload_info = dbapi.upload_get_by_catalog_id(catalog)
                if upload_info:
                    for upload in upload_info:
                        dbapi.uoload_destroy(upload['id'])
        return redirect(url_for('admin_index'))
    return render_template('catalog.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/user_signout', methods=['GET', 'POST'])
def user_signout():
    if not g.user:
        abort(401)

    flash('您已经退出登录')
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/user_signin', methods=['GET', 'POST'])
def user_signin():
    if request.method == 'POST':
        pwd = request.form.get('password', None)
        e = request.form.get('email', None)
        if e and pwd:
            new_pwd = baseutils.hash_password(pwd)
            user_info = dbapi.user_get_by_email(e)
        else:
            error = "需要输入Email。"
            return render_template('signin.html', error=error)
        
        if new_pwd == user_info['password']:
            flash("欢迎回来： %s" % user_info['name'])
            session['user_id'] = user_info['id']
            return redirect(url_for('index'))
        else:
            error = "密码有误！"
            return render_template('signin.html', error=error)
    return render_template('signin.html')

@app.route('/admin_user_edit/', methods=['GET', 'POST'])
def admin_user_edit():
    if not g.user:
        abort(401)

    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', None)
        pwd_rp = request.form.get('passwordRp', None)
        
        if pwd == pwd_rp:
            new_pwd = baseutils.hash_password(pwd)
            print new_pwd
        else:
            error = "两次输入的密码不同，请重新确认！"
            return redirect('admin_index', error=error)

        user_info = {'name': request.form.get('user_name', None),
                     'password': new_pwd}

        for k,v in user_info.items():
            if not v:
                del user_info[k]
        
        dbapi.user_update(1, user_info)
    return redirect(url_for('admin_index'))

@app.route('/admin/', methods=['GET', 'POST'])
@app.route('/admin/<error>')
def admin_index(error=None):
    if not g.user:
        abort(401)
        
    try:
        catalogs = dbapi.catalog_get_all()
        catalog_num = len(catalogs)
    except:
        return render_template('admin_index.html')
    if request.method == 'POST':
        site_info = {'name': request.form.get('site_name', None)}
        for k,v in site_info.items():
            if not v:
                del site_info[k]        
        if site_info:
            dbapi.site_update(1, site_info)

    return render_template('admin_index.html', catalogs=catalogs, 
                           catalog_num=catalog_num, error=error)

@app.route('/init_db/create/')
def init_db():
    if not g.user:
        abort(401)

    _ENGINE = db_session.get_engine()
    db_init.db_manage(_ENGINE, method='init')
    default_site_info = {'name': '海龟终结者',
                         'title': '海龟终结者的独白',
                         'description': 'long long ago'}
    default_catalog_info = {'name': "默认分类"}
    pwd = baseutils.hash_password('123456')
    user_info = {'email': "tpiperatgod@gmail.com",
                 'name': 'admin',
                 'password': pwd}
    dbapi.site_create(default_site_info)
    dbapi.catalog_create(default_catalog_info)
    dbapi.user_create(user_info)
    session['db_status'] = 1
    return redirect(url_for('index'))

@app.route('/init_db/drop/')
def drop_db():
    if not g.user:
        abort(401)

    _ENGINE = db_session.get_engine()
    db_init.db_manage(_ENGINE, method='drop')
    session['db_status'] = 0
    return redirect(url_for('index'))

@app.errorhandler(401)
def four_zero_one(error):
    return render_template('401.html'), 401

@app.errorhandler(404)
def four_zero_four(error):
    return render_template('404.html'), 404