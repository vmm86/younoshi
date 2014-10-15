#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import fn, JOIN_LEFT_OUTER

from model import Season, Age, Stage, Team, SAS, SAST, GP

from User import login_required

## Игровые протоколы
@login_required
def listGP(seasonid, ageid, sasid):
    listSeason = Season.select().order_by(Season.season_ID.asc())
    try:
        seasonname = Season.get(season_ID = seasonid).seasonName
    except Season.DoesNotExist:
        seasonname = None

    listAge = Age.select().order_by(Age.ageName)
    try:
        agename = Age.get(age_ID = ageid).ageName
    except Age.DoesNotExist:
        agename = None

    try:
        sastype = SAS.get(SAS.SAS_ID == sasid).stage_ID.stageType
    except SAS.DoesNotExist:
        sastype = None

    try:
        sasgametype = SAS.get(SAS.SAS_ID == sasid).gameType_ID.gameTypeName
    except SAS.DoesNotExist:
        sasgametype = None

    listSAS_Z = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "Z").order_by(Stage.stageName)
    listSAS_G = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "G").order_by(Stage.stageName)
    listSAS_P = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage).where(Stage.stageType == "P").order_by(Stage.stageName)

    listSAST = SAST.select().where(SAST.SAS_ID == sasid).join(Team).switch(SAST).join(Stage, JOIN_LEFT_OUTER).order_by(Team.teamName)    
    listGP   = GP.select().join(SAST).where(SAST.SAS_ID == sasid).order_by(GP.GP_ID)

    # Для тестирования в консоли из старой модели
    # maxvalues = GameProtocol.select(fn.Max(GameProtocol.gameNumber).alias('gnmax'), fn.Max(GameProtocol.tourNumber).alias('tnmax'), fn.Max(GameProtocol.gameDate).alias('dmax')).join(SeasonAgeStageTeam, JOIN_LEFT_OUTER).where(SeasonAgeStageTeam.SAS_ID == sasid)

    # Удобства при создании новых матчей

    maxvalues = GP.select(fn.Max(GP.gameNumber).alias('gnmax'), fn.Max(GP.tourNumber).alias('tnmax'), fn.Max(GP.gameDate).alias('dmax')).join(SAST).where(SAST.SAS_ID == sasid).naive()

    for i in maxvalues:
        try:
            ## Номер матча - по умолчанию на 1 больше, чем последний добавленный либо 1
            gnmax = int(i.gnmax)
            ## Номер тура - по умолчанию такой же, как последний добавленный либо 1
            tnmax = int(i.tnmax)
            ## Дата матча - по умолчанию такая же, как последняя добавленная либо сегодняшняя
            ## Дата в форме выводится в формате ДД.ММ.ГГГГ, а в БД записывается в формате ГГГГ-ММ-ДД
            dmax  = i.dmax
            dmax = dmax.strftime('%d.%m.%Y')
        except TypeError:
            gnmax = 0
            tnmax = 1
        except AttributeError:
            dmax = datetime.datetime.now().strftime('%d.%m.%Y')
        finally:
            gnmax += 1

    return render_template(
        'GP.jinja.html', 
        listSeason  = listSeason,
        seasonid    = seasonid,
        listAge     = listAge,
        ageid       = ageid,
        listSAS_Z   = listSAS_Z,
        listSAS_G   = listSAS_G,
        listSAS_P   = listSAS_P,
        sasid       = sasid,
        sastype     = sastype,
        sasgametype = sasgametype,
        listSAST    = listSAST,
        listGP      = listGP,
        gnmax       = gnmax,
        tnmax       = tnmax,
        dmax        = dmax)

### Добавление игрового протокола
@login_required
def createGP(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'create':
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

        gamedate = datetime.datetime.strptime(request.form['gameDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

        htid     = request.form['filterHT']
        gtid     = request.form['filterGT']

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
            issemifinal = bool(int(request.form['is_Semifinal']))
        except KeyError:
            issemifinal = False

        try:
            isfinal = bool(int(request.form['is_Final']))
        except KeyError:
            isfinal = False

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
                is_Semifinal       = issemifinal, 
                is_Final           = isfinal)

        return redirect(
            url_for('listGP',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))

### Изменение игрового протокола
@login_required
def updateGP(seasonid, ageid, sasid, gpid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        gameNumber = request.form['gameNumber']

        try:
            tournumber = request.form['tourNumber']
        except KeyError:
            tournumber = 0
        if tournumber == '':
            tournumber = 0
 
        try:
            stageNumber = request.form['stageNumber']
        except KeyError:
            stageNumber = None
        if stageNumber == '':
            stageNumber = None

        gameDate = datetime.datetime.strptime(request.form['gameDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

        homeTeam_ID  = request.form['filterHT']
        guestTeam_ID = request.form['filterGT']

        homeTeamScoreGame = request.form['HTscoreGame']
        if homeTeamScoreGame == '':
            homeTeamScoreGame = None

        guestTeamScoreGame = request.form['GTscoreGame']
        if guestTeamScoreGame == '':
            guestTeamScoreGame = None

        try:
            homeTeamScore11m = request.form['HTscore11m']
        except KeyError:
            homeTeamScore11m = None
        if homeTeamScore11m == '':
            homeTeamScore11m = None

        try:
            guestTeamScore11m = request.form['GTscore11m']
        except KeyError:
            guestTeamScore11m = None
        if guestTeamScore11m == '':
            guestTeamScore11m = None

        try:
            is_Semifinal = bool(int(request.form['is_Semifinal']))
        except KeyError:
            is_Semifinal = False

        try:
            is_Final = bool(int(request.form['is_Final']))
        except KeyError:
            is_Final = False

        if session['demo']:
            pass
        else:
            GP        = GP()
            GP.GP_ID  = gpid

            # Заготовка для отслеживания только изменённых значений при обновлении
            # GPfields  = GP._meta.fields
            # currentGP = GP.get(GP_ID = gpid)
            # for field in GPfields:
            #     if '{0}.{1}'.format(currentGP, field) != field:
            #         '{0}.{1}'.format(GP, field) = field

            GP.gameNumber         = gameNumber
            GP.tourNumber         = tourNumber
            GP.stageNumber        = stageNumber
            GP.gameDate           = gameDate
            GP.homeTeam_ID        = homeTeam_ID
            GP.guestTeam_ID       = guestTeam_ID
            GP.homeTeamScoreGame  = homeTeamScoreGame
            GP.guestTeamScoreGame = guestTeamScoreGame
            GP.homeTeamScore11m   = homeTeamScore11m
            GP.guestTeamScore11m  = guestTeamScore11m
            GP.is_Semifinal       = is_Semifinal
            GP.is_Final           = is_Final
            GP.save()

        return redirect(
            url_for('listGP',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))

### Удаление игрового протокола
@login_required
def deleteGP(seasonid, ageid, sasid, gpid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            GP.get(GP_ID = gpid).delete_instance()

        return redirect(
            url_for('listGP',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))
