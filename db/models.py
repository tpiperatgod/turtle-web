#!/usr/bin/env python
#*-*coding:utf-8*-*
#coding=utf-8
import os, sys

from sqlalchemy import Column, Integer, BigInteger, String, schema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship, backref, object_mapper

sys.path.append("..")
from utils import timeutils
from session import get_session
from dbapi import Base

class WebBase(object):

    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    created_at = Column(DateTime, default=timeutils.utcnow)
    updated_at = Column(DateTime, onupdate=timeutils.utcnow)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        
        try:
            session.flush()
        except IntegrityError, e:
            if str(e).endswith('is not unique'):
                raise exception.Duplicate(str(e))
            else:
                raise

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = timeutils.utcnow()
        self.save(session=session)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        columns = dict(object_mapper(self).columns).keys()
        if hasattr(self, '_extra_keys'):
            columns.extend(self._extra_keys())
        self._i = iter(columns)
        return self

    def next(self):
        n = self._i.next()
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict"""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()
    
class User(Base, WebBase):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), unique=True)
    name = Column(String(255))
    password = Column(String(255))    

class Site(Base, WebBase):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))
    title = Column(String(255))
    description = Column(String(2000))

class Upload(Base, WebBase):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))
    name = Column(String(255))
    description = Column(String(2000), nullable=True, default='...')
    catalog = Column(Integer, default=1)
    url = Column(String(2000))
    path = Column(String(2000))
    heat = Column(Integer)
    types = Column(String(255))
    
class Catalog(Base, WebBase):
    __tablename__ = 'catalogs'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255))

class Comment(Base, WebBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    pic_id = Column(Integer)
    name = Column(String(255))
    content = Column(String(2000), nullable=False)
    
    
    
    
    
    
