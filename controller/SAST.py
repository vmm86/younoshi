#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import JOIN_LEFT_OUTER

from model import City, School, Team, Season, Age, Stage, SeasonAgeStage, SeasonAgeStageTeam

from User import login_required

## Команды в игровых этапах
@login_required
def listSAST(seasonid, ageid, sasid):
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
        sastype = SeasonAgeStage.get(SeasonAgeStage.SAS_ID == sasid).stage_ID.stageType
    except SeasonAgeStage.DoesNotExist:
        sastype = None

    listSAS_Z = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "Z").order_by(Stage.stageName)
    listSAS_G = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "G").order_by(Stage.stageName)
    listSAS_P = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "P").order_by(Stage.stageName)

    filterCity   =   City.select().order_by(City.cityName)
    filterSchool = School.select().order_by(School.schoolName)
    filterTeam   =   Team.select().order_by(Team.teamName)

    listSAST  = SeasonAgeStageTeam.select().where(SeasonAgeStageTeam.SAS_ID == sasid).join(Stage, JOIN_LEFT_OUTER).order_by(SeasonAgeStageTeam.SAST_ID)
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName).order_by(Stage.stage_ID)

    is_SASTsubstage  = SeasonAgeStageTeam.select().where(SeasonAgeStageTeam.SAS_ID == sasid).join(Stage).exists()
    listSASTsubstage = SeasonAgeStageTeam.select(SeasonAgeStageTeam.substage_ID).distinct().where(SeasonAgeStageTeam.SAS_ID == sasid).join(Stage, JOIN_LEFT_OUTER)

    return render_template(
        'SAST.jinja.html', 
        listSeason       = listSeason,
        seasonid         = seasonid,
        seasonname       = seasonname,
        listAge          = listAge,
        ageid            = ageid,
        agename          = agename,
        listSAS_Z        = listSAS_Z,
        listSAS_G        = listSAS_G,
        listSAS_P        = listSAS_P,
        sasid            = sasid,
        sastype          = sastype,
        filterCity       = filterCity,
        filterSchool     = filterSchool,
        filterTeam       = filterTeam,
        listSAST         = listSAST,
        listStage        = listStage,
        is_SASTsubstage  = is_SASTsubstage,
        listSASTsubstage = listSASTsubstage)

### Добавление команд в игровые этапы
@login_required
def createSAST(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        teamid     = request.form['filterTeam']
        substageid = request.form['substage_ID']

        # В шаблоне в input для значения NULL д.б. указано value=""
        if substageid:
            pass
            substageid
        else:
            substageid = None

        if session['demo']:
            pass
        else:
            SeasonAgeStageTeam.create(
                SAS_ID      = sasid, 
                team_ID     = teamid, 
                substage_ID = substageid)

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))

### Изменение команд в игровых этапах
@login_required
def updateSAST(seasonid, ageid, sasid, sastid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        teamid     = request.form['filterTeam']
        substageid = request.form['substage_ID']

        # В шаблоне в input для значения NULL д.б. указано value=""
        if substageid:
            pass
            substageid
        else:
            substageid = None

        if session['demo']:
            pass
        else:
            SAST             = SeasonAgeStageTeam()
            SAST.SAST_ID     = sastid
            SAST.team_ID     = teamid
            SAST.substage_ID = substageid
            SAST.save()

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))

### Удаление команд в игровых этапах
@login_required
def deleteSAST(seasonid, ageid, sasid, sastid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешним ключам FK_HT_SAST и FK_GT_SAST 
            # не позволяет удалить команду в игровом этапе при наличии связанных с ней матчей.
            try:
                SeasonAgeStageTeam.get(SAST_ID = sastid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту команду, пока с её участием добавлен хотя бы один матч', 'danger')

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid))
