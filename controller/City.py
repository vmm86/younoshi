#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER, IntegrityError

from model import City, School

from User import login_required

# Города
@login_required
def listCity():
    # Вывод списка городов и количества их дочерних школ
    listCity = City.select(City, fn.Count(School.city_ID).alias('countSchools')).join(School, JOIN_LEFT_OUTER).group_by(City).order_by(City.cityName)

    # Переменные для автозаполнения формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['cityName']
    ## Заголовки модального окна
    createHeader = ['"Создать новый населённый пункт"']
    updateHeader = ['"Изменить "', 'cityName']
    ## Действия формы
    createAction = ['"/city/create"']
    updateAction = ['"/city/"', 'PK_ID', '"/update"']
    deleteAction = ['"/city/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'City.jinja.html', 
        listCity     = listCity,
        modifyFields = modifyFields,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление городов
@login_required
def createCity():
    # Получение полей формы из шаблона
    cityname = request.form['cityName']

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        City.create(
            cityName = cityname)

    # Редирект на вид list
    return redirect(
        url_for('listCity'))

### Изменение городов
@login_required
def updateCity(cityid):
    # Получение полей формы из шаблона
    cityname = request.form['cityName']

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        city          = City()
        city.city_ID  = cityid
        city.cityName = cityname
        city.save()

    # Редирект на вид list
    return redirect(
        url_for('listCity'))

### Удаление городов
@login_required
def deleteCity(cityid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_School_City 
        # не позволяет удалить населённый пункт при наличии связанных с ним спортивных школ.
        try:
            City.get(city_ID = cityid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить этот город, пока в него добавлена хотя бы одна спортивная школа', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listCity'))
