#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER, DoesNotExist, IntegrityError

from model import City, School, Team

from User import login_required

# Спортивные школы
@login_required
def listSchool(cityid):
    # Список городов, название текущего города
    listCity = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except DoesNotExist:
        cityname = None

    # Список школ и количества их дочерних команд
    listSchool = School.select(School, fn.Count(Team.school_ID).alias('countTeams')).join(Team, JOIN_LEFT_OUTER).switch(School).join(City).where(City.city_ID == cityid).group_by(School).order_by(School.schoolName)

    # Переменные для автозаполнения модальной формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['schoolName', 'cityName']
    ## Заголовки модального окна
    createHeader = ['"Создать новую спортивную школу"']
    updateHeader = ['"Изменить "', 'schoolName', '" ("', 'cityName', '")"']
    ## Действия формы
    createAction = ['"/city/"', cityid, '"/school/create"']
    updateAction = ['"/city/"', cityid, '"/school/"', 'PK_ID', '"/update"']
    deleteAction = ['"/city/"', cityid, '"/school/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'School.jinja.html', 
        listCity   = listCity, 
        cityid     = cityid, 
        cityname   = cityname, 
        listSchool = listSchool,
        modifyFields = modifyFields,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление спортивных школ
@login_required
def createSchool(cityid):
    # Получение полей формы из шаблона
    schoolname = request.form['schoolName']

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        School.create(
            city_ID = cityid, 
            schoolName = schoolname
        )

    # Редирект на вид list
    return redirect(
        url_for('listSchool', 
            cityid = cityid))

### Изменение споривных школ
@login_required
def updateSchool(cityid, schoolid):
    # Получение полей формы из шаблона
    schoolname = request.form['schoolName']

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        school            = School()
        school.school_ID  = schoolid
        school.city_ID    = cityid
        school.schoolName = schoolname
        school.save()

    # Редирект на вид list
    return redirect(
        url_for('listSchool', 
            cityid = cityid))

### Удаление спортивных школ
@login_required
def deleteSchool(cityid, schoolid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_Team_School 
        # не позволяет удалить спортивную школу при наличии связанных с ней команд
        try:
            School.get(city_ID = cityid, school_ID = schoolid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить эту спортивную школу, пока в неё добавлена хотя бы одна команда', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listSchool', 
            cityid = cityid))
