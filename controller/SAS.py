#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import RawQuery, fn, JOIN_LEFT_OUTER, DoesNotExist, IntegrityError

from model import Season, Age, Stage, GameType, SAS, SAST, GP

from User import login_required

## Игровые этапы
@login_required
def listSAS(seasonid, ageid):
    # Список сезонов и возрастов, название текущего сезона и возраста
    listSeason = Season.select().order_by(Season.season_ID.asc())
    listAge    = Age.select().order_by(Age.ageName)
    try:
        seasonname = Season.get(season_ID = seasonid).seasonName
        agename    = Age.get(age_ID = ageid).ageName
    except DoesNotExist:
        seasonname = None
        agename    = None

    # Список игровых стадий
    listStage    = Stage.select().order_by(Stage.stageType, Stage.stageName)
    # Список типов соревноавний
    listGameType = GameType.select().order_by(GameType.gameTypeName)
    # Список игровых этапов с количеством дочерних команд и матчей
    listSAS = (RawQuery(SAS, 
        'SELECT `SAS`.*, (SELECT COUNT(`SAST2`.`SAS_ID`) FROM `SeasonAgeStageTeam` AS `SAST2` WHERE `SAST2`.`SAS_ID` = `SAS`.`SAS_ID`) AS `countSAST`, (SELECT COUNT(`GP2`.`SAS_ID`) FROM `GameProtocol` AS `GP2` WHERE ((`GP2`.`SAS_ID` = `SAST`.`SAS_ID`) AND (`SAST`.`SAS_ID` = `SAS`.`SAS_ID` ))) AS `countGP` FROM `SeasonAgeStage` AS `SAS` LEFT JOIN `SeasonAgeStageTeam` AS `SAST` ON (`SAS`.`SAS_ID` = `SAST`.`SAS_ID`) LEFT JOIN `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) WHERE ((`SAS`.`season_ID` = %s) AND (`SAS`.`age_ID` = %s)) GROUP BY `SAS`.`SAS_ID` ORDER BY `SAS`.`SAS_ID` ASC', seasonid, ageid))

    # Переменные для автозаполнения формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['stage', 'zoneGroupPlayoffToggle', 'gameType', 'startDate', 'finishDate']
    ## Список групп радиокнопок
    modifyRadios = ['zoneGroupPlayoffToggle', 'gameType']
    ## Список групп радиокнопок
    modifySelect = ['stage']   
    ## Заголовки модального окна
    createHeader = ['"Создать новую игровую стадию"']
    updateHeader = ['"Изменить игровую стадию для возраста "', agename, '" в сезоне "', seasonname]
    ## Действия формы
    createAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/create"']
    updateAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/"', 'PK_ID', '"/update"']
    deleteAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/"', 'PK_ID', '"/delete"']

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
        listSAS      = listSAS,
        modifyFields = modifyFields,
        modifyRadios = modifyRadios,
        modifySelect = modifySelect,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление игровых этапов
@login_required
def createSAS(seasonid, ageid):
    # Получение полей формы из шаблона
    stageid    = request.form['stage']
    gametype   = request.form['gameType']
    try:
        startdate  = request.form['startDate']
        finishdate = request.form['finishDate']
    except DoesNotExist:
        startdate  = None
        finishdate = None

    if startdate:
        startdate  = datetime.datetime.strptime(startdate,  '%d.%m.%Y').strftime('%Y-%m-%d')
    if finishdate:
        finishdate = datetime.datetime.strptime(finishdate, '%d.%m.%Y').strftime('%Y-%m-%d')

    # Сохранение новой записи в БД
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
                finishDate  = finishdate)
        except IntegrityError:
            flash('Вы не можете добавить ещё один такой же игровой этап в одном и том же сезоне и возрасте', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listSAS',
            seasonid = seasonid,
            ageid    = ageid))

### Изменение игровых этапов
@login_required
def updateSAS(seasonid, ageid, sasid):
    # Получение полей формы из шаблона
    stageid    = request.form['stage']
    gametype   = request.form['gameType']
    try:
        startdate  = request.form['startDate']
        finishdate = request.form['finishDate']
    except DoesNotExist:
        startdate  = None
        finishdate = None

    if startdate:
        startdate  = datetime.datetime.strptime(startdate,  '%d.%m.%Y').strftime('%Y-%m-%d')
    if finishdate:
        finishdate = datetime.datetime.strptime(finishdate, '%d.%m.%Y').strftime('%Y-%m-%d')

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        sas             = SAS()
        sas.SAS_ID      = sasid
        sas.season_ID   = seasonid
        sas.age_ID      = ageid
        sas.stage_ID    = stageid
        sas.gameType_ID = gametype
        sas.startDate   = startdate
        sas.finishDate  = finishdate
        sas.save()

    # Редирект на вид list
    return redirect(
        url_for('listSAS',
            seasonid = seasonid,
            ageid    = ageid))

### Удаление игровых этапов
@login_required
def deleteSAS(seasonid, ageid, sasid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_SAST_SAS 
        # не позволяет удалить игровой этап при наличии связанных с ним дочерних команд.
        try:
            SAS.get(SAS_ID = sasid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить этот игровой этап, пока в него добавлена хотя бы одна команда', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listSAS',
            seasonid = seasonid,
            ageid    = ageid))
