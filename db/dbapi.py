#!/bin/python
#
#

import re
import time
from session import get_session
import sys
sys.path.append("..")
from utils import timeutils

from sqlalchemy import create_engine
import sqlalchemy.interfaces
import sqlalchemy.orm
from sqlalchemy.pool import NullPool, StaticPool
from sqlalchemy.exc import DisconnectionError, OperationalError, \
                            IntegrityError
from sqlalchemy.orm import relationship, backref, object_mapper, \
                            joinedload, joinedload_all, \
                            scoped_session, sessionmaker
from sqlalchemy import and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import asc, desc, literal_column
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, BigInteger, String, schema
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, Float

Base = declarative_base()
import models

def init_db():
    Base.metadata.create_all(bind=engine)
    
def model_query(model, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id. If set to 'allow_none',
            restriction includes project_id = None.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or 'no'

    query = session.query(model, *args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
                _("Unrecognized read_deleted value '%s'") % read_deleted)

    return query

def make_dict(f):
    """Make the model object behave like a dict.

    Includes attributes from joins."""
    def __dict__(*args):
        res = f(*args)
        local = dict(res)
        return local
    return __dict__

def make_dict_for_all(f):
    """Make the model object behave like a dict.

    Includes attributes from joins."""
    def __dict__(*args):
        res = f(*args)
        local = [dict(res[i]) for i in range(len(res))]
        return local
    return __dict__


########### user models api #############

def user_create(values):
    user_ref = models.User()
    user_ref.update(values)
    
    session = get_session()
    try:
        with session.begin():
            user_ref.save(session=session)
    except IntegrityError, e:
        raise e
#         msg = 'error %s' % e
#         raise msg
    return user_ref

def user_destroy(user_id):
    db_session.query(models.User).\
            filter_by(id=user_id).\
            update({'deleted': True,
                    'deleted_at': timeutils.utcnow(),
                    'updated_at': literal_column('updated_at')})
    db_session.commit()

@make_dict
def user_get(user_id):
    return _user_get(user_id, session=None)

def _user_get(user_id, session=None):

    result = model_query(models.User, session=session, read_deleted='no').\
                filter_by(id=user_id).\
                first()
    return result

@make_dict
def user_get_by_email(user_email):
    return _user_get_by_email(user_email, session=None)

def _user_get_by_email(user_email, session=None):

    result = model_query(models.User, session=session, read_deleted='no').\
                filter_by(email=user_email).\
                first()
    return result

@make_dict_for_all
def user_get_all():
    return _user_get_all(session=None)

def _user_get_all(session=None):
    result = model_query(models.User, session=session, read_deleted='no').\
                all()
    return result

def user_update(user_id, values):
    session = get_session()
    with session.begin():
        user_ref = _user_get(user_id, session=session)
        user_ref.update(values)
        user_ref.save(session=session)
     
########### site models api #############

def site_create(values):
    site_ref = models.Site()
    site_ref.update(values)
    
    session = get_session()
    try:
        with session.begin():
            site_ref.save(session=session)
    except IntegrityError, e:
        raise e
#         msg = 'error %s' % e
#         raise msg
    return site_ref

@make_dict
def site_get(site_id):
    return _site_get(site_id, session=None)

def _site_get(site_id, session=None):

    result = model_query(models.Site, session=session, read_deleted='no').\
                filter_by(id=site_id).\
                first()
    return result

def site_update(site_id, values):
    session = get_session()
    with session.begin():
        site_ref = _site_get(site_id, session=session)
        site_ref.update(values)
        site_ref.save(session=session)
        
########### user models api #############

def upload_create(values):
    upload_ref = models.Upload()
    upload_ref.update(values)
    
    session = get_session()
    try:
        with session.begin():
            upload_ref.save(session=session)
    except IntegrityError, e:
        raise e
#         msg = 'error %s' % e
#         raise msg
    return upload_ref

def uoload_destroy(upload_id):
    session = get_session()
    with session.begin():   
        session.query(models.Upload).\
                filter_by(id=upload_id).\
                update({'deleted': True,
                        'deleted_at': timeutils.utcnow(),
                        'updated_at': literal_column('updated_at')})

@make_dict
def upload_get(upload_id):
    return _upload_get(upload_id, session=None)

def _upload_get(upload_id, session=None):

    result = model_query(models.Upload, session=session, read_deleted='no').\
                filter_by(id=upload_id).\
                first()
    return result

@make_dict_for_all
def upload_get_by_catalog_id(upload_catalog_id):
    return _upload_get_by_catalog_id(upload_catalog_id, session=None)

def _upload_get_by_catalog_id(upload_catalog_id, session=None):

    result = model_query(models.Upload, session=session, read_deleted='no').\
                filter_by(catalog=upload_catalog_id).\
                all()
    return result

@make_dict
def upload_get_by_url(upload_url):
    return _upload_get_by_url(upload_url, session=None)

def _upload_get_by_url(upload_url, session=None):

    result = model_query(models.Upload, session=session, read_deleted='no').\
                filter_by(url=upload_url).\
                first()
    return result

@make_dict_for_all
def upload_get_all():
    return _upload_get_all(session=None)

def _upload_get_all(session=None):
    result = model_query(models.Upload, session=session, read_deleted='no').\
                all()
    return result


def upload_update(upload_id, values):
    session = get_session()
    with session.begin():
        upload_ref = _upload_get(upload_id, session=session)
        upload_ref.update(values)
        upload_ref.save(session=session)


########### catalog models api #############

def catalog_create(values):
    catalog_ref = models.Catalog()
    catalog_ref.update(values)
    
    session = get_session()
    try:
        with session.begin():
            catalog_ref.save(session=session)
    except IntegrityError, e:
        raise e
#         msg = 'error %s' % e
#         raise msg
    return catalog_ref

def catalog_destroy(catalog_id):
    session = get_session()
    with session.begin():    
        session.query(models.Catalog).\
                filter_by(id=catalog_id).\
                update({'deleted': True,
                        'deleted_at': timeutils.utcnow(),
                        'updated_at': literal_column('updated_at')})

@make_dict
def catalog_get(catalog_id):
    return _catalog_get(catalog_id, session=None)

def _catalog_get(catalog_id, session=None):

    result = model_query(models.Catalog, session=session, read_deleted='no').\
                filter_by(id=catalog_id).\
                first()
    return result

@make_dict
def catalog_get_by_name(catalog_name):
    return _catalog_get_by_name(catalog_name, session=None)

def _catalog_get_by_name(catalog_name, session=None):

    result = model_query(models.Catalog, session=session, read_deleted='no').\
                filter_by(name=catalog_name).\
                first()
    return result

@make_dict
def catalog_get_by_id(catalog_id):
    return _catalog_get_by_id(catalog_id, session=None)

def _catalog_get_by_id(catalog_id, session=None):

    result = model_query(models.Catalog, session=session, read_deleted='no').\
                filter_by(id=catalog_id).\
                first()
    return result

@make_dict_for_all
def catalog_get_all():
    return _catalog_get_all(session=None)

def _catalog_get_all(session=None):
    result = model_query(models.Catalog, session=session, read_deleted='no').\
                all()
    return result


def catalog_update(catalog_id, values):
    session = get_session()
    with session.begin():
        catalog_ref = _catalog_get(catalog_id, session=session)
        catalog_ref.update(values)
        catalog_ref.save(session=session)
        
########### comments models api #############

def comment_create(values):
    comment_ref = models.Comment()
    comment_ref.update(values)
    
    session = get_session()
    try:
        with session.begin():
            comment_ref.save(session=session)
    except IntegrityError, e:
        raise e
#         msg = 'error %s' % e
#         raise msg
    return comment_ref

def comment_destroy(comment_id):
    session = get_session()
    with session.begin():    
        session.query(models.Comment).\
                filter_by(id=comment_id).\
                update({'deleted': True,
                        'deleted_at': timeutils.utcnow(),
                        'updated_at': literal_column('updated_at')})

@make_dict
def comment_get(comment_id):
    return _comment_get(comment_id, session=None)

def _comment_get(comment_id, session=None):

    result = model_query(models.Comment, session=session, read_deleted='no').\
                filter_by(id=comment_id).\
                first()
    return result