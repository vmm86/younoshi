#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import IntegrityError

from model import Season

from User import login_required

## Сезоны
@login_required
def listSeason():
    # Вывод списка сезонов
    listSeason = Season.select().order_by(Season.seasonName)

    # Переменные для автозаполнения формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['seasonName']
    ## Заголовки модального окна
    createHeader = ['"Создать новый сезон"']
    updateHeader = ['"Изменить "', 'seasonName']
    ## Действия формы
    createAction = ['"/season/create"']
    updateAction = ['"/season/"', 'PK_ID', '"/update"']
    deleteAction = ['"/season/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'Season.jinja.html', 
        listSeason = listSeason,
        modifyFields = modifyFields,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление сезонов
@login_required
def createSeason():
    # Получение полей формы из шаблона
    seasonname = request.form['seasonName']

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        Season.create(
            seasonName = seasonname)

    # Редирект на вид list
    return redirect(
        url_for('listSeason'))

### Изменение сезонов
@login_required
def updateSeason(seasonid):
    # Получение полей формы из шаблона
    seasonname = request.form['seasonName']

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        season            = Season()
        season.season_ID  = seasonid
        season.seasonName = seasonname
        season.save()

    # Редирект на вид list
    return redirect(
        url_for('listSeason'))

### Удаление сезонов
@login_required
def deleteSeason(seasonid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_SAS_Season 
        # не позволяет удалить стадию при наличии связанных с ней игровых этапов.
        try:
            Season.get(season_ID = seasonid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить этот сезон, пока в нём добавлен хотя бы один игровой этап', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listSeason'))
