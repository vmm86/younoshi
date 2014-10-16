#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER, DoesNotExist

from model import Season, Age, Stage, GameType, SAS, SAST, GP

from User import login_required

## Игровые этапы
@login_required
def listSAS(seasonid, ageid):
    listSeason = Season.select().order_by(Season.season_ID.asc())

    listAge = Age.select().order_by(Age.ageName)

    try:
        seasonname = Season.get(season_ID = seasonid).seasonName
        agename    = Age.get(age_ID = ageid).ageName
    except DoesNotExist:
        seasonname = None
        agename    = None

    listStage    = Stage.select().order_by(Stage.stageType, Stage.stageName)
    listGameType = GameType.select().order_by(GameType.gameTypeName)
    listSAS      = (SAS
        .select(SAS, 
            fn.Count(fn.Distinct(SAST.SAST_ID)).alias('countSAST'), 
            fn.Count(GP.GP_ID).alias('countGP')) 
        .join(SAST, JOIN_LEFT_OUTER).join(GP, JOIN_LEFT_OUTER)
        .switch(SAS).join(Stage)
        .where(SAS.season_ID == seasonid, SAS.age_ID == ageid)
        .group_by(SAS)
        .order_by(Stage.stageName, SAS.gameType_ID).naive())

    return render_template(
        'SAS.jinja.html', 
        listSeason   = listSeason,
        seasonid     = seasonid,
        seasonname   = seasonname,
        listAge      = listAge,
        ageid        = ageid,
        agename      = agename,
        listStage    = listStage,
        listGameType = listGameType,
        listSAS      = listSAS)

### Добавление игровых этапов
@login_required
def createSAS(seasonid, ageid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        stageid    = request.form['stage']
        gametype   = request.form['gameType']
        startdate  = datetime.datetime.strptime(request.form['startDate'],  '%d.%m.%Y').strftime('%Y-%m-%d')
        finishdate = datetime.datetime.strptime(request.form['finishDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

        if session['demo']:
            pass
        else:
            # Ограничение по ключу UNIQUE_Season_Age_Stage 
            # не позволяет добавить повторяющуюся комбинацию сезон/возраст/стадия в игровом этапе.
            # Например, нельзя добавить второй этап плэй-офф в одном и том же сезоне и возрасте.
            try:
                SAS.create(
                    season_ID   = seasonid, 
                    age_ID      = ageid, 
                    stage_ID    = stageid, 
                    gameType_ID = gametype,
                    startDate   = startdate,
                    finishDate  = finishdate
                )
            except IntegrityError:
                flash('Вы не можете добавить ещё один такой же игровой этап в одном и том же сезоне и возрасте', 'danger')

        return redirect(
            url_for('listSAS',
                seasonid = seasonid,
                ageid    = ageid))

### Изменение игровых этапов
@login_required
def updateSAS(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        stageid    = request.form['stage']
        gametype   = request.form['gameType']
        startdate  = datetime.datetime.strptime(request.form['startDate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        finishdate = datetime.datetime.strptime(request.form['finishDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

        if session['demo']:
            pass
        else:
            SAS             = SAS()
            SAS.SAS_ID      = sasid
            SAS.season_ID   = seasonid
            SAS.age_ID      = ageid
            SAS.stage_ID    = stageid
            SAS.gameType_ID = gametype
            SAS.startDate   = startdate
            SAS.finishDate  = finishdate
            SAS.save()

        return redirect(
            url_for('listSAS',
                seasonid = seasonid,
                ageid    = ageid))

### Удаление игровых этапов
@login_required
def deleteSAS(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAST_SAS 
            # не позволяет удалить игровой этап при наличии связанных с ним дочерних команд.
            try:
                SAS.get(SAS_ID = sasid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот игровой этап, пока в него добавлена хотя бы одна команда', 'danger')

        return redirect(
            url_for('listSAS',
                seasonid = seasonid,
                ageid    = ageid))
