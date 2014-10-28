#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER

from model import City, School

from User import login_required

## Города
@login_required
def listCity():
    listCity = City.select(City, fn.Count(School.city_ID).alias('countSchools')).join(School, JOIN_LEFT_OUTER).group_by(City).order_by(City.cityName)

    return render_template(
        'City.jinja.html', 
        listCity = listCity)

### Добавление городов
@login_required
def createCity():
    if request.method == 'POST' and request.form['modify'] == 'create':
        cityname = request.form['cityName']

        if session['demo']:
            pass
        else:
            City.create(
                cityName = cityname)

        return redirect(
            url_for('listCity'))

### Изменение городов
@login_required
def updateCity(cityid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        cityname = request.form['cityName']

        if session['demo']:
            pass
        else:
            city          = City()
            city.city_ID  = cityid
            city.cityName = cityname
            city.save()

        return redirect(
            url_for('listCity'))

### Удаление городов
@login_required
def deleteCity(cityid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_School_City 
            # не позволяет удалить населённый пункт при наличии связанных с ним спортивных школ.
            try:
                City.get(city_ID = cityid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот город, пока в него добавлена хотя бы одна спортивная школа', 'danger')

        return redirect(
            url_for('listCity'))
