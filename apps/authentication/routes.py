# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for , session 
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, UpdateProfileForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass
import pandas as pd
import bcrypt
import tensorflow as tf
import numpy as np
@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            logged_user = login_user(user)
            session['plan'] = user.plan
            session['user_id'] = user.id

            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    
    print(session['user_id'])

    return redirect(url_for('home_blueprint.index'))



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        print(create_account_form)
        username = create_account_form.username.data
        password = create_account_form.password.data
        email = create_account_form.email.data
        plan = create_account_form.plan.data
        favorite_news = create_account_form.favorite_news.data
        favorite_stocks = create_account_form.favorite_stocks.data
        favorite_influancer = create_account_form.favorite_influancer.data

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        #user = Users(**request.form)
        user = Users(username=username,password=password,email=email,plan=plan,favorite_news=favorite_news,favorite_stocks=favorite_stocks,favorite_influancer=favorite_influancer)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)



@blueprint.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    update_profile_form = UpdateProfileForm(request.form)   
    profile_data = Users.query.get_or_404(id)

    news_favorite = profile_data.favorite_news.split(',')

    print(news_favorite)

    if 'profile' in request.form:
        news = request.form.getlist('favorite_news')
        stocks = request.form.getlist('favorite_stocks')
        influencers = request.form.getlist('favorite_influencer')
        profile_data.username = update_profile_form.username.data
        if update_profile_form.password.data :
            profile_data.password = update_profile_form.password.data
        profile_data.email = update_profile_form.email.data
        profile_data.plan = update_profile_form.plan.data
        profile_data.favorite_news = ','.join([str(news_item) for news_item in news ])
        profile_data.favorite_stocks = ','.join([str(stocks_item) for stocks_item in stocks ])
        profile_data.favorite_influencer = ','.join([str(influencer_item) for influencer_item in influencers ])

        # Check usename exists

        # Check email exists
        #user = Users.query.filter_by(email=email).first()
        #if user:
        #    return render_template('accounts/profile.html',
        #                           msg='Email already registered',
        #                           success=False,
        #                           form=update_profile_form)

        # else we can create the user
        #user = Users(**request.form)
        #user = Users(username=username,password=password,email=email,plan=plan,favorite_news=favorite_news,favorite_stocks=favorite_stocks,favorite_influancer=favorite_influancer)
        #db.session.add(user)
        db.session.commit()

        return render_template('accounts/profile.html',
                               msg='You Profile Updated!',
                               success=True,
                               form=update_profile_form, segment='profile',profile_data=profile_data)

    else:
        return render_template('accounts/profile.html', form=update_profile_form,profile_data=profile_data, segment='profile')




@blueprint.route('/logout')
def logout():
    logout_user()
    session.pop('plan', None)
    session.pop('user_id', None)
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


@blueprint.route('/getHelloText', methods=['GET'])
def getHelloText():
    return "HELLLLO"

@blueprint.route('/getQuarterlySetniment', methods=['GET'])
def getQuarterlySetniment():
    data = pd.read_csv("apps/data/apple_news_quarterly.csv")
    
    return data.to_json()

@blueprint.route('/getMonthlySetniment', methods=['GET'])
def getMonthlySetniment():
    data = pd.read_csv("apps/data/apple_news_monthly.csv")
    
    return data.to_json()

@blueprint.route('/getAppleData', methods=['GET'])
def getAppleData():
    data = pd.read_csv("apps/data/apple_data.csv")
    model = tf.keras.models.load_model('apps/data/models/model.hdf5')
    X_train = []
    seq_len = 32
    data_2 = data[['close', 'high', 'low', 'open', 'volume', 'NN', 'NP']].values
    for i in range(seq_len, len(data_2)):
        X_train.append(data_2[i-seq_len:i])

    X_train = np.array(X_train)

    
    data['EC'] = np.concatenate((np.zeros(32), model.predict(X_train)), axis=None)
    return data.to_json()

@blueprint.route('/ticker/getNews/<ticker_id>', methods=['GET'])
def getTickerNewsData(ticker_id=None):
    if str(ticker_id) == "1":
        data = pd.read_csv("apps/data/news.csv")
    if str(ticker_id) == "2":
        data = pd.read_csv("apps/data/amazon_data.csv")
    
    return data.to_json()        

@blueprint.route('/getAllNews', methods=['GET'])
def getAllNews():
    data = pd.read_csv("apps/data/annotated_news.csv")
    
    return data.to_json()