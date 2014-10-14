#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER

from model import City, School, Team

from User import login_required

## Спортивные школы
@login_required
def listSchool(cityid):
    listCity = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except City.DoesNotExist:
        cityname = None

    listSchool = School.select(School, fn.Count(Team.school_ID).alias('countTeams')).join(Team, JOIN_LEFT_OUTER).switch(School).join(City).where(City.city_ID == cityid).group_by(School).order_by(School.schoolName)

    return render_template(
        'School.jinja.html', 
        listCity   = listCity, 
        cityid     = cityid, 
        cityname   = cityname, 
        listSchool = listSchool)

### Добавление спортивных школ
@login_required
def createSchool(cityid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        schoolname = request.form['schoolName']

        if session['demo']:
            pass
        else:
            School.create(
                city_ID = cityid, 
                schoolName = schoolname
            )

        return redirect(
            url_for('listSchool', 
                cityid = cityid))

### Изменение споривных школ
@login_required
def updateSchool(cityid, schoolid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        schoolname = request.form['schoolName']

        if session['demo']:
            pass
        else:
            school            = School()
            school.school_ID  = schoolid
            school.city_ID    = cityid
            school.schoolName = schoolname
            school.save()

        return redirect(
            url_for('listSchool', 
                cityid = cityid))

### Удаление спортивных школ
@login_required
def deleteSchool(cityid, schoolid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_Team_School 
            # не позволяет удалить спортивную школу при наличии связанных с ней команд.
            try:
                School.get(city_ID = cityid, school_ID = schoolid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту спортивную школу, пока в неё добавлена хотя бы одна команда', 'danger')

        return redirect(
            url_for('listSchool', 
                cityid = cityid))
