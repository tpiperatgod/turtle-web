#!/usr/bin/env python
#*-*coding:utf-8*-*
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Float, ForeignKey
from sqlalchemy import Index, Integer, MetaData, String, Table, Text
from sqlalchemy import dialects
import sys

sys.path.append("..")
import logging
import logging.config

LOG = logging.getLogger(__name__)

def MediumText():
    return Text().with_variant(dialects.mysql.MEDIUMTEXT(), 'mysql')

def db_manage(migrate_engine, method=None):
    meta = MetaData()
    meta.bind = migrate_engine

    user = Table('user', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        Column('email', String(length=255), unique=True),
        Column('name', String(length=255)),
        Column('password', String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
    
    site = Table('site', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(length=255)),
        Column('title', String(length=255)),
        Column('description', String(length=2000)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
    
    uploads = Table('uploads', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(length=255)),
        Column('title', String(length=255)),
        Column('description', String(length=2000), nullable=True),
        Column('catalog', Integer),
        Column('url', String(length=2000)),
        Column('path', String(length=2000)),
        Column('heat', Integer),
        Column('types', String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'                    
    
    )

    catalogs = Table('catalogs', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'                    
    
    )
    
    comments = Table('comments', meta,
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        Column('deleted', Boolean),
        Column('id', Integer, primary_key=True, nullable=False),
        Column('pic_id', Integer),
        Column('name', String(length=255)),
        Column('content', String(length=2000), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'                    
    
    )
    # create all tables
    tables = [user, site, uploads, catalogs, comments]
    
    if method == 'init':
        for table in tables:
            try:
                table.create()
            except Exception:
                LOG.info(repr(table))
                LOG.exception('Exception while creating table.')
                raise ArithmeticError
    
    elif method == 'drop':
        for table in tables:
            try:
                table.drop()
            except Exception:
                LOG.info(repr(table))
                LOG.exception('Exception while droping table.')
                raise ArithmeticError        
    