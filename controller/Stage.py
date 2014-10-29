#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import IntegrityError

from model import Stage

from User import login_required

# Стадии
@login_required
def listStage():
    # Вывод списка игровых стадий
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)

    # Переменные для автозаполнения формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['stageType', 'stageName']
    ## Список групп радиокнопок
    modifyRadios = ['stageType']
    ## Заголовки модального окна
    createHeader = ['"Создать новую игровую стадию"']
    updateHeader = ['"Изменить "', 'stageName']
    ## Действия формы
    createAction = ['"/stage/create"']
    updateAction = ['"/stage/"', 'PK_ID', '"/update"']
    deleteAction = ['"/stage/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'Stage.jinja.html', 
        listStage = listStage,
        modifyFields = modifyFields,
        modifyRadios = modifyRadios,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление стадий
@login_required
def createStage():
    # Получение полей формы из шаблона
    stagetype = request.form['stageType']
    stagename = request.form['stageName']

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        Stage.create(
            stageType = stagetype, 
            stageName = stagename)

    # Редирект на вид list
    return redirect(
        url_for('listStage'))

### Изменение стадий
@login_required
def updateStage(stageid):
    # Получение полей формы из шаблона
    stagetype = request.form['stageType']
    stagename = request.form['stageName']

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        stage           = Stage()
        stage.stage_ID  = stageid
        stage.stageType = stagetype
        stage.stageName = stagename
        stage.save()

    # Редирект на вид list
    return redirect(
        url_for('listStage'))

### Удаление стадий
@login_required
def deleteStage(stageid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_SAS_Stage 
        # не позволяет удалить стадию при наличии связанных с ней игровых этапов.
        try:
            Stage.get(stage_ID = stageid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить эту стадию, пока с ней связан хотя бы один игровой этап внутри сезона', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listStage'))
