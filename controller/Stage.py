#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import Stage

from User import login_required

## Стадии
@login_required
def listStage():
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)

    return render_template(
        'Stage.jinja.html', 
        listStage = listStage)

### Добавление стадий
@login_required
def createStage():
    if request.method == 'POST' and request.form['modify'] == 'create':
        stagetype = request.form['stageType']
        stagename = request.form['stageName']

        if session['demo']:
            pass
        else:
            Stage.create(
                stageType = stagetype, 
                stageName = stagename)

        return redirect(
            url_for('listStage'))

### Изменение стадий
@login_required
def updateStage(stageid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        stagetype = request.form['stageType']
        stagename = request.form['stageName']

        if session['demo']:
            pass
        else:
            stage           = Stage()
            stage.stage_ID  = stageid
            stage.stageType = stagetype
            stage.stageName = stagename
            stage.save()

        return redirect(
            url_for('listStage'))

### Удаление стадий
@login_required
def deleteStage(stageid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAS_Stage 
            # не позволяет удалить стадию при наличии связанных с ней игровых этапов.
            try:
                Stage.get(stage_ID = stageid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту стадию, пока с ней связан хотя бы один игровой этап внутри сезона', 'danger')

        return redirect(
            url_for('listStage'))
