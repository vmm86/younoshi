#! /usr/bin/python
# -*- coding: utf-8 -*-

from exceptions import TypeError, AttributeError, KeyError

from datetime import date, datetime

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER, DoesNotExist, IntegrityError

from model import Season, Age, Stage, Team, SAS, SAST, GP

from User import login_required

## Игровые протоколы
@login_required
def listGP(seasonid, ageid, sasid):
    # Список сезонов и возрастов, название текущего сезона и возраста, название и тип игровой стадии текущего игрового этапа, тип текущего соревнования
    listSeason = Season.select().order_by(Season.season_ID.asc())
    listAge = Age.select().order_by(Age.ageName)
    for age in listAge:
        age.ageName = int(date.today().year) - int(age.ageName)
    try:
        seasonname  = Season.get(season_ID = seasonid).seasonName
        agename     = Age.get(age_ID = ageid).ageName
        sasname     = SAS.get(SAS_ID = sasid).stage_ID.stageName
        sastype     = SAS.get(SAS_ID = sasid).stage_ID.stageType
        sasgametype = SAS.get(SAS_ID = sasid).gameType_ID.gameTypeName
    except DoesNotExist:
        seasonname  = None
        agename     = None
        sasname     = None
        sastype     = None
        sasgametype = None

    # Список игровых этапов по типам
    listSAS_Z = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "Z").order_by(Stage.stageName)
    listSAS_G = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "G").order_by(Stage.stageName)
    listSAS_P = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "P").order_by(Stage.stageName)

    # Список команд в текущем игровом этапе
    listSAST = SAST.select().where(SAST.SAS_ID == sasid).join(Team).switch(SAST).join(Stage, JOIN_LEFT_OUTER).order_by(Team.teamName)
    # Список матчей в текущем игровом этапе
    listGP   = GP.select().distinct().join(SAST, on=GP.SAS_ID).where((SAST.SAS_ID == sasid) & (GP.SAS_ID == sasid)).order_by(GP.gameNumber)

    # Удобства при создании новых матчей

    maxvalues = GP.select(fn.Max(GP.gameNumber).alias('gnmax'), fn.Max(GP.tourNumber).alias('tnmax'), fn.Max(GP.gameDate).alias('dmax')).where((SAST.SAS_ID == sasid) & (GP.SAS_ID == sasid)).join(SAST).scalar(as_tuple = True)

    try:
        ## Номер матча - по умолчанию на 1 больше, чем последний добавленный либо 1
        gnmax = int(maxvalues[0])
        ## Номер тура - по умолчанию такой же, как последний добавленный либо 1
        tnmax = int(maxvalues[1])
        ## Дата матча - по умолчанию такая же, как последняя добавленная либо сегодняшняя
        ## Дата в форме выводится в формате ДД.ММ.ГГГГ, а в БД записывается в формате ГГГГ-ММ-ДД
        dmax  = (maxvalues[2]).strftime('%d.%m.%Y')
    except (TypeError, AttributeError):
        gnmax = 0
        tnmax = 1
        dmax  = datetime.now().strftime('%d.%m.%Y')
    finally:
        gnmax += 1

    # Переменные для автозаполнения формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['gameNumber', 'tourNumber', 'stageNumber', 'gameDate', 'filterHT', 'filterGT', 'HTscoreGame', 'GTscoreGame', 'HTscore11m', 'GTscore11m', 'is_Semifinal', 'is_Final', 'stageType', 'stageName']
    ## Список групп чекбоксов
    modifyChkbox = ['is_Semifinal', 'is_Final']
    ## Список групп радиокнопок
    modifyRadios = ['stageNumber']
    ## Список выпадающих списков
    modifySelect = ['filterHT', 'filterGT']   
    ## Заголовки модального окна
    createHeader = ['"Добавить новый матч в "', 'stageType', '" "', 'stageName']
    updateHeader = ['"Изменить матч в "', 'stageType', '" "', 'stageName']
    ## Действия формы
    createAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/"', sasid, '"/gp/create"']
    updateAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/"', sasid, '"/gp/"', 'PK_ID', '"/update"']
    deleteAction = ['"/season/"', seasonid, '"/age/"', ageid, '"/stage/"', sasid, '"/gp/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'GP.jinja.html', 
        listSeason   = listSeason,
        seasonid     = seasonid,
        listAge      = listAge,
        ageid        = ageid,
        listSAS_Z    = listSAS_Z,
        listSAS_G    = listSAS_G,
        listSAS_P    = listSAS_P,
        sasid        = sasid,
        sasname      = sasname,
        sastype      = sastype,
        sasgametype  = sasgametype,
        listSAST     = listSAST,
        listGP       = listGP,
        gnmax        = gnmax,
        tnmax        = tnmax,
        dmax         = dmax,
        modifyChkbox = modifyChkbox,
        modifyFields = modifyFields,
        modifyRadios = modifyRadios,
        modifySelect = modifySelect,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление игрового протокола
@login_required
def createGP(seasonid, ageid, sasid):
    # Получение полей формы из шаблона
    gamenumber = request.form['gameNumber']

    try:
        tournumber = request.form['tourNumber']
    except KeyError:
        tournumber = 0
    if tournumber == '':
        tournumber = 0

    try:
        stagenumber = request.form['stageNumber']
    except KeyError:
        stagenumber = None
    if stagenumber == '':
        stagenumber = None

    gamedate = datetime.strptime(request.form['gameDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

    htid = request.form['filterHT']
    gtid = request.form['filterGT']

    htscoregame = request.form['HTscoreGame']
    if htscoregame == '':
        htscoregame = None

    gtscoregame = request.form['GTscoreGame']
    if gtscoregame == '':
        gtscoregame = None

    try:
        htscore11m = request.form['HTscore11m']
    except KeyError:
        htscore11m = None
    if htscore11m == '':
        htscore11m = None

    try:
        gtscore11m = request.form['GTscore11m']
    except KeyError:
        gtscore11m = None
    if gtscore11m == '':
        gtscore11m = None

    try:
        is_semifinal = bool(int(request.form['is_Semifinal']))
    except KeyError:
        is_semifinal = False

    try:
        is_final = bool(int(request.form['is_Final']))
    except KeyError:
        is_final = False

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        GP.create(
            gameNumber         = gamenumber, 
            tourNumber         = tournumber, 
            stageNumber        = stagenumber, 
            gameDate           = gamedate, 
            homeTeam_ID        = htid, 
            guestTeam_ID       = gtid, 
            homeTeamScoreGame  = htscoregame, 
            guestTeamScoreGame = gtscoregame, 
            homeTeamScore11m   = htscore11m, 
            guestTeamScore11m  = gtscore11m, 
            is_Semifinal       = is_semifinal, 
            is_Final           = is_final,
            SAS_ID             = sasid)

    # Редирект на вид list
    return redirect(
        url_for('listGP',
            seasonid = seasonid,
            ageid    = ageid,
            sasid    = sasid))

### Изменение игрового протокола
@login_required
def updateGP(seasonid, ageid, sasid, gpid):
    # Получение полей формы из шаблона
    gamenumber = request.form['gameNumber']

    try:
        tournumber = request.form['tourNumber']
    except KeyError:
        tournumber = 0
    if tournumber == '':
        tournumber = 0

    try:
        stagenumber = request.form['stageNumber']
    except KeyError:
        stagenumber = None
    if stagenumber == '':
        stagenumber = None

    gamedate = datetime.strptime(request.form['gameDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

    htid = request.form['filterHT']
    gtid = request.form['filterGT']

    htscoregame = request.form['HTscoreGame']
    if htscoregame == '':
        htscoregame = None

    gtscoregame = request.form['GTscoreGame']
    if gtscoregame == '':
        gtscoregame = None

    try:
        htscore11m = request.form['HTscore11m']
    except KeyError:
        htscore11m = None
    if htscore11m == '':
        htscore11m = None

    try:
        gtscore11m = request.form['GTscore11m']
    except KeyError:
        gtscore11m = None
    if gtscore11m == '':
        gtscore11m = None

    try:
        is_semifinal = bool(int(request.form['is_Semifinal']))
    except KeyError:
        is_semifinal = False

    try:
        is_final = bool(int(request.form['is_Final']))
    except KeyError:
        is_final = False

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        gp        = GP()
        gp.GP_ID  = gpid

        # Заготовка для отслеживания только изменённых значений при обновлении
        # GPfields  = GP._meta.fields
        # currentGP = GP.get(GP_ID = gpid)
        # for field in GPfields:
        #     if '{0}.{1}'.format(currentGP, field) != field:
        #         '{0}.{1}'.format(GP, field) = field

        gp.gameNumber         = gamenumber
        gp.tourNumber         = tournumber
        gp.stageNumber        = stagenumber
        gp.gameDate           = gamedate
        gp.homeTeam_ID        = htid
        gp.guestTeam_ID       = gtid
        gp.homeTeamScoreGame  = htscoregame
        gp.guestTeamScoreGame = gtscoregame
        gp.homeTeamScore11m   = htscore11m
        gp.guestTeamScore11m  = gtscore11m
        gp.is_Semifinal       = is_semifinal
        gp.is_Final           = is_final
        gp.SAS_ID             = sasid
        gp.save()

    # Редирект на вид list
    return redirect(
        url_for('listGP',
            seasonid = seasonid,
            ageid    = ageid,
            sasid    = sasid))

### Удаление игрового протокола
@login_required
def deleteGP(seasonid, ageid, sasid, gpid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        GP.get(GP_ID = gpid).delete_instance()

    # Редирект на вид list
    return redirect(
        url_for('listGP',
            seasonid = seasonid,
            ageid    = ageid,
            sasid    = sasid))
