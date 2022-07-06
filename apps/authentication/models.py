# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt
from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    plan = db.Column(db.Integer)
    favorite_news = db.Column(db.String(64))
    favorite_stocks= db.Column(db.String(64))
    favorite_influencer = db.Column(db.String(64))

        
    '''
    @property
    def favorite_news(self):
        return [ str(n) for n in self._favorite_news.split(';')]
    @favorite_news.setter
    def favorite_news(self, value):
        self._favorite_news += ';%s' % value


    @property
    def favorite_stocks(self):
        return [ str(s) for s in self._favorite_stocks.split(';')]
    @favorite_stocks.setter
    def favorite_stocks(self, value):
        self._favorite_stocks += ';%s' % value
  
    @property
    def favorite_influencer(self):
        return [ str(f) for f in self._favorite_influencer.split(';')]
    @favorite_influencer.setter
    def favorite_influencer(self, value):
        self._favorite_influencer += ';%s' % value
    '''
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class StockHistory(db.Model, UserMixin):
    __tablename__ = 'stock_history'

    stock = db.Column(db.String(32), primary_key=True)
    date = db.Column(db.DateTime(), primary_key=True)
    close = db.Column(db.Float())
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    volume = db.Column(db.Float())


class News(db.Model, UserMixin):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String())
    date = db.Column(db.DateTime())