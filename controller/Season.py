#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import Season

from User import login_required

## Сезоны
@login_required
def listSeason():
    listSeason = Season.select().order_by(Season.seasonName)

    return render_template(
        'Season.jinja.html', 
        listSeason = listSeason)

### Добавление сезонов
@login_required
def createSeason():
    if request.method == 'POST' and request.form['modify'] == 'create':
        seasonname = request.form['seasonName']

        if session['demo']:
            pass
        else:
            Season.create(
                seasonName = seasonname)

        return redirect(
            url_for('listSeason'))

### Изменение сезонов
@login_required
def updateSeason(seasonid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        seasonname = request.form['seasonName']

        if session['demo']:
            pass
        else:
            season            = Season()
            season.season_ID  = seasonid
            season.seasonName = seasonname
            season.save()

        return redirect(
            url_for('listSeason'))

### Удаление сезонов
@login_required
def deleteSeason(seasonid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAS_Season 
            # не позволяет удалить стадию при наличии связанных с ней игровых этапов.
            try:
                Season.get(season_ID = seasonid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот сезон, пока в нём добавлен хотя бы один игровой этап', 'danger')

        return redirect(
            url_for('listSeason'))
