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

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    users = Table('users', meta,
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
    
    # create all tables
    tables = [users, site]

    for table in tables:
        try:
            table.create()
        except Exception:
            LOG.info(repr(table))
            LOG.exception('Exception while creating table.')
            raise ArithmeticError

