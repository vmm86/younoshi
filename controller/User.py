#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps

from hashlib import md5

from flask import session, render_template, url_for, request, redirect, abort, flash

from peewee import DoesNotExist

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import User

# Авторизация
def auth_user(user):
    session['logged_in'] = True
    session['user_ID']   = user.user_ID
    session['userLogin'] = user.userLogin
    if session['userLogin'] == 'demo':
        session['demo'] = True
    else:
        session['demo'] = None
    session['userName'] = user.userName
    flash('Вы успешно вошли в систему как %s' % (user.userName), 'success')

# Декоратор проверяет сессию.
# Если пользователь не вошёл в систему, он перенаправляется на вид login.
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(
                url_for('login'))
        return f(*args, **kwargs)
    return inner

# Получаем объект, соответствующий запросу или страницу ошибки 404.
# Используется алиас вызова метода "GET" из модели, 
# который получает объект или выдаёт исключение DoesNotExist.
def get_object_or_404(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        abort(404)
        return render_template('404.jinja.html')

## Обработка ошибки 400
# def key_error(e):
#     flash('К сожалению, ваш запрос не удалось выполнить. \
#     Попробуйте сделать это ещё раз, введя все необходимые данные.', 'danger')
#     return render_template(
#         'index.jinja.html'), 400

## Обработка ошибки 404
@login_required
def page_not_found(error):
    return render_template(
        '404.jinja.html'), 404

## Главная страница
@login_required
def index():
    return render_template('index.jinja.html')

## Вход в систему
def login():
    if session.get('logged_in') and session['logged_in'] == True:
        return redirect(
            url_for('index'), 
            code=302)
    else:
        if request.method == 'POST' and request.form['login']:
            try:
                userlogin = request.form['userLogin']
                userpassw = md5(request.form['userPassword']).hexdigest()
                user      = User.get(userLogin = userlogin, userPassword = userpassw)
            except User.DoesNotExist:
                flash('Имя или пароль введёны неправильно - попробуйте ещё раз', 'danger')
            else:
                auth_user(user)
                return redirect(
                    url_for('index'))

    return render_template('login.jinja.html')

## Выход из системы
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы', 'warning')
    return redirect(
        url_for('index'))
