#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from flask import redirect, request, session, url_for, abort, render_template, flash

from functools import wraps

from hashlib import md5

from model import *

# from werkzeug.wrappers import BaseRequest
# from werkzeug.wsgi import responder
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, default_exceptions

from younoshi import app

app.secret_key = config.SECRET_KEY

# Авторизация
def auth_user(user):
    session['logged_in'] = True
    session['user_ID']   = user.user_ID
    session['userLogin'] = user.userLogin
    if session['userLogin'] == 'demo':
        session['demo'] = True
    else:
        session['demo'] = None
    session['userName'] = user.userName
    flash('Вы успешно вошли в систему как %s' % (user.userName), 'success')

# Декоратор проверяет сессию.
# Если пользователь не вошёл в систему, он перенаправляется на вид login.
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(
                url_for('login'))
        return f(*args, **kwargs)
    return inner

# Получаем объект, соответствующий запросу или страницу ошибки 404.
# Используется алиас вызова метода "GET" из модели, который получает одиночный объект 
# или выдаёт исключение DoesNotExist, если ни одного такого объекта не найдено.
def get_object_or_404(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        abort(404)
        return render_template('404.jinja.html')

## Обработка ошибки 400
def key_error(e):
    flash('К сожалению, ваш запрос не удалось выполнить. Попробуйте сделать это ещё раз, введя все необходимые данные.', 'danger')
    return render_template(
        'index.jinja.html'), 400

## Обработка ошибки 404
@app.errorhandler(404)
@login_required
def page_not_found(error):
    return render_template(
        '404.jinja.html'), 404

## Главная страница
@app.route('/')
@login_required
def index():
    ### В зависимости от того, вошёл пользователь в систему или нет, ему показывается стартовая страница.
    return render_template(
        'index.jinja.html')

## Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['login']:
        try:
            userlogin = request.form['userLogin']
            userpassw = md5(request.form['userPassword']).hexdigest()
            user      = User.get(userLogin = userlogin, userPassword = userpassw)
        except User.DoesNotExist:
            flash('Имя или пароль введёны неправильно - попробуйте ещё раз', 'danger')
        else:
            auth_user(user)
            return redirect(
                url_for('index')
            )

    return render_template('login.jinja.html')

## Выход из системы
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы', 'warning')
    return redirect(
        url_for('index')
    )

## Города
@app.route('/city')
@login_required
def listCity():
    listCity = City.select(City, fn.Count(School.city_ID).alias('countSchools')).join(School, JOIN_LEFT_OUTER).group_by(City).order_by(City.cityName)

    return render_template(
        'City.jinja.html', 
        listCity = listCity
    )

### Добавление городов
@app.route('/city/create', methods=['GET', 'POST'])
@login_required
def createCity():
    if request.method == 'POST' and request.form['modify'] == 'create':
        cityname = request.form['cityName']

        if session['demo']:
            pass
        else:
            City.create(
                cityName = cityname
            )

        return redirect(
            url_for('listCity')
        )

### Изменение городов
@app.route('/city/<int:cityid>/update', methods = ['GET', 'POST'])
@login_required
def updateCity(cityid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        cityname = request.form['cityName']

        if session['demo']:
            pass
        else:
            city          = City()
            city.city_ID  = cityid
            city.cityName = cityname
            city.save()

        return redirect(
            url_for('listCity')
        )

### Удаление городов
@app.route('/city/<int:cityid>/delete', methods = ['GET', 'POST'])
@login_required
def deleteCity(cityid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_School_City не позволяет удалить населённый пункт при наличии связанных с ним спортивных школ.
            try:
                City.get(city_ID = cityid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот город, пока в него добавлена хотя бы одна спортивная школа', 'danger')

        return redirect(
            url_for('listCity')
        )

## Спортивные школы
@app.route('/city/<int:cityid>/school')
@login_required
def listSchool(cityid):
    listCity = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except City.DoesNotExist:
        cityname = None

    listSchool = School.select(School, fn.Count(Team.school_ID).alias('countTeams')).join(Team, JOIN_LEFT_OUTER).switch(School).join(City).where(City.city_ID == cityid).group_by(School).order_by(School.schoolName)

    return render_template(
        'School.jinja.html', 
        listCity   = listCity, 
        cityid     = cityid, 
        cityname   = cityname, 
        listSchool = listSchool
    )

### Добавление спортивных школ
@app.route('/city/<int:cityid>/school/create', methods = ['GET', 'POST'])
@login_required
def createSchool(cityid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        schoolname = request.form['schoolName']

        if session['demo']:
            pass
        else:
            School.create(
                city_ID = cityid, 
                schoolName = schoolname
            )

        return redirect(
            url_for('listSchool', 
                cityid = cityid
            )
        )

### Изменение споривных школ
@app.route('/city/<int:cityid>/school/<int:schoolid>/update', methods = ['GET', 'POST'])
@login_required
def updateSchool(cityid, schoolid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        schoolname = request.form['schoolName']

        if session['demo']:
            pass
        else:
            school            = School()
            school.school_ID  = schoolid
            school.city_ID    = cityid
            school.schoolName = schoolname
            school.save()

        return redirect(
            url_for('listSchool', 
                cityid = cityid
            )
        )

### Удаление спортивных школ
@app.route('/city/<int:cityid>/school/<int:schoolid>/delete', methods = ['GET', 'POST'])
@login_required
def deleteSchool(cityid, schoolid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_Team_School не позволяет удалить спортивную школу при наличии связанных с ней команд.
            try:
                School.get(city_ID = cityid, school_ID = schoolid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту спортивную школу, пока в неё добавлена хотя бы одна команда', 'danger')

        return redirect(
            url_for('listSchool', 
                cityid = cityid
            )
        )

## Команды
@app.route('/city/<int:cityid>/school/<int:schoolid>/team')
@login_required
def listTeam(cityid, schoolid):
    listCity = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except City.DoesNotExist:
        cityname = None

    listSchool = School.select().join(City).where(City.city_ID == cityid).order_by(School.schoolName)
    try:
        schoolname = School.get(school_ID = schoolid).schoolName
    except School.DoesNotExist:
        schoolname = None

    listAge  = Age.select().order_by(Age.ageName)
    listTeam = Team.select().join(School).where(School.school_ID == schoolid).join(City).where(City.city_ID == cityid).order_by(Team.teamName)

    return render_template(
        'Team.jinja.html', 
        listCity   = listCity, 
        cityid     = cityid, 
        cityname   = cityname, 
        listSchool = listSchool, 
        schoolid   = schoolid, 
        schoolname = schoolname,
        listAge    = listAge, 
        listTeam   = listTeam
    )

### Добавление команд
@app.route('/city/<int:cityid>/school/<int:schoolid>/team/create', methods = ['GET', 'POST'])
@login_required
def createTeam(cityid, schoolid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        teamname = request.form['teamName']
        ageid    = request.form['age_ID']

        if session['demo']:
            pass
        else:
            Team.create(
                school_ID = schoolid, 
                age_ID = ageid, 
                teamName = teamname
            )

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid
            )
        )

### Изменение команд
@app.route('/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/update', methods = ['GET', 'POST'])
@login_required
def updateTeam(cityid, schoolid, teamid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        teamname = request.form['teamName']
        ageid    = request.form['age_ID']

        if session['demo']:
            pass
        else:
            team           = Team()
            team.team_ID   = teamid
            team.school_ID = schoolid
            team.age_ID    = ageid
            team.teamName  = teamname
            team.save()

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid,
                teamid   = teamid
            )
        )

### Удаление команд
@app.route('/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/delete', methods = ['GET', 'POST'])
@login_required
def deleteTeam(cityid, schoolid, teamid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAST_Team не позволяет удалить команду при наличии связанных с ней игровых этапов.
            try:
                Team.get(school_ID = schoolid, team_ID = teamid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту команду, пока она добавлена хотя бы в один игровой этап', 'danger')

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid,
                teamid   = teamid
            )
        )

## Стадии
@app.route('/stage')
@login_required
def listStage():
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)

    return render_template(
        'Stage.jinja.html', 
        listStage = listStage
    )

### Добавление стадий
@app.route('/stage/create', methods = ['GET', 'POST'])
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
                stageName = stagename
            )

        return redirect(
            url_for('listStage')
        )

### Изменение стадий
@app.route('/stage/<int:stageid>/update', methods = ['GET', 'POST'])
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
            url_for('listStage')
        )

### Удаление стадий
@app.route('/stage/<int:stageid>/delete', methods = ['GET', 'POST'])
@login_required
def deleteStage(stageid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAS_Stage не позволяет удалить стадию при наличии связанных с ней игровых этапов в определённом сезоне и возрасте.
            try:
                Stage.get(stage_ID = stageid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту стадию, пока с ней связан хотя бы один игровой этап внутри сезона', 'danger')

        return redirect(
            url_for('listStage')
        )

## Сезоны
@app.route('/season')
@login_required
def listSeason():
    listSeason = Season.select().order_by(Season.seasonName)

    return render_template(
        'Season.jinja.html', 
        listSeason = listSeason
    )

### Добавление сезонов
@app.route('/season/create', methods = ['GET', 'POST'])
@login_required
def createSeason():
    if request.method == 'POST' and request.form['modify'] == 'create':
        seasonname = request.form['seasonName']

        if session['demo']:
            pass
        else:
            Season.create(
                seasonName = seasonname
            )

        return redirect(
            url_for('listSeason')
        )

### Изменение сезонов
@app.route('/season/<int:seasonid>/update', methods = ['GET', 'POST'])
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
            url_for('listSeason')
        )

### Удаление сезонов
@app.route('/season/<int:seasonid>/delete', methods = ['GET', 'POST'])
@login_required
def deleteSeason(seasonid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAS_Season не позволяет удалить стадию при наличии связанных с ней игровых этапов в определённом сезоне и возрасте.
            try:
                Season.get(season_ID = seasonid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот сезон, пока в нём добавлен хотя бы один игровой этап', 'danger')

        return redirect(
            url_for('listSeason')
        )

## Игровые стадии
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage')
@login_required
def listSAS(seasonid, ageid):
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

    listStage    = Stage.select().order_by(Stage.stageType, Stage.stageName)
    listGameType = GameType.select().order_by(GameType.gameTypeName)
    listSAS      = SeasonAgeStage.select(SeasonAgeStage, fn.Count(SeasonAgeStageTeam.SAS_ID).alias('countSAST'), fn.Count(GameProtocol.homeTeam_ID).alias('countHT'), fn.Count(GameProtocol.guestTeam_ID).alias('countGT')).where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(SeasonAgeStageTeam, JOIN_LEFT_OUTER).join(GameProtocol, JOIN_LEFT_OUTER).switch(SeasonAgeStage).join(Stage).group_by(SeasonAgeStage).order_by(Stage.stageName, SeasonAgeStage.gameType_ID)

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
        listSAS      = listSAS
    )

### Добавление игровых этапов
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/create', methods=['GET', 'POST'])
@login_required
def createSAS(seasonid, ageid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        stageid    = request.form['stage']
        gametype   = request.form['gameType']
        startdate  = datetime.datetime.strptime(request.form['startDate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        finishdate = datetime.datetime.strptime(request.form['finishDate'], '%d.%m.%Y').strftime('%Y-%m-%d')

        if session['demo']:
            pass
        else:
            # Ограничение по ключу UNIQUE_Season_Age_Stage не позволяет добавить повторяющуюся комбинацию сезон/возраст/стадия в рамках игрового этапа.
            # Например, нельзя добавить второй этап плэй-офф в одном и том же сезоне и возрасте.
            try:
                SeasonAgeStage.create(
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
                ageid    = ageid
            )
        )

### Изменение игровых этапов
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/update', methods = ['GET', 'POST'])
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
            SAS             = SeasonAgeStage()
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
                ageid    = ageid
            )
        )

### Удаление игровых этапов
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/delete', methods  = ['GET', 'POST'])
@login_required
def deleteSAS(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAST_SAS не позволяет удалить игровой этап при наличии связанных с ним дочерних команд.
            try:
                SeasonAgeStage.get(SAS_ID = sasid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот игровой этап, пока в него добавлена хотя бы одна команда', 'danger')

        return redirect(
            url_for('listSAS',
                seasonid = seasonid,
                ageid    = ageid
            )
        )

## Команды в игровых этапах
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team')
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
        listSASTsubstage = listSASTsubstage
    )

### Добавление команд в игровые этапы
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/create', methods=['GET', 'POST'])
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
                substage_ID = substageid
            )

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )

### Изменение команд в игровых этапах
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/<int:sastid>/update', methods=['GET', 'POST'])
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
                sasid    = sasid
            )
        )

### Удаление команд в игровых этапах
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/<int:sastid>/delete', methods  = ['GET', 'POST'])
@login_required
def deleteSAST(seasonid, ageid, sasid, sastid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешним ключам FK_HT_SAST и FK_GT_SAST не позволяет удалить команду в игровом этапе при наличии связанных с ней матчей.
            try:
                SeasonAgeStageTeam.get(SAST_ID = sastid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту команду, пока с её участием добавлен хотя бы один матч', 'danger')

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )

## Игровые протоколы
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp')
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

    sasid = sasid
    try:
        sastype = SeasonAgeStage.get(SeasonAgeStage.SAS_ID == sasid).stage_ID.stageType
    except SeasonAgeStage.DoesNotExist:
        sastype = None

    try:
        sasgametype = SeasonAgeStage.get(SeasonAgeStage.SAS_ID == sasid).gameType_ID.gameTypeName
    except SeasonAgeStage.DoesNotExist:
        sasgametype = None

    listSAS_Z = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "Z").order_by(Stage.stageName)
    listSAS_G = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "G").order_by(Stage.stageName)
    listSAS_P = SeasonAgeStage.select().where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(Stage).where(Stage.stageType == "P").order_by(Stage.stageName)

    listSAST = SeasonAgeStageTeam.select().where(SeasonAgeStageTeam.SAS_ID == sasid).join(Team).switch(SeasonAgeStageTeam).join(Stage, JOIN_LEFT_OUTER).order_by(SeasonAgeStageTeam.SAST_ID)
    listGP   = GameProtocol.select().join(SeasonAgeStageTeam).where(SeasonAgeStageTeam.SAS_ID == sasid).order_by(GameProtocol.GP_ID)

    # Удобства при создании новых матчей
    ## Номер матча - по умолчанию на 1 больше, чем последний добавленный либо 1
    try:
        gnmax = int(GameProtocol.select(fn.Max(GameProtocol.gameNumber)).scalar())
    except TypeError:
        gnmax = 0
    finally:
        gnmax += 1
    ## Номер тура - по умолчанию такой же, как последний добавленный либо 1
    try:
        tnmax = int(GameProtocol.select(fn.Max(GameProtocol.tourNumber)).scalar())
    except TypeError:
        tnmax = 1
    ## Дата матча - по умолчанию такая же, как последняя добавленная либо сегодняшняя
    ## Дата в форме выводится в формате ДД.ММ.ГГГГ, а в БД записывается в формате ГГГГ-ММ-ДД
    try:
        dmax = GameProtocol.select(fn.Max(GameProtocol.gameDate)).scalar()
        dmax = dmax.strftime('%d.%m.%Y')
    except AttributeError:
        dmax = datetime.datetime.now().strftime('%d.%m.%Y')

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
        dmax        = dmax
    )

### Добавление игрового протокола
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/create', methods=['GET', 'POST'])
@login_required
def createGP(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        gamenumber = request.form['gameNumber']
        tournumber = request.form['tourNumber']
 
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
            GameProtocol.create(
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
                is_Final           = isfinal
            )

        return redirect(
            url_for('listGP',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )

### Изменение игрового протокола
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/<int:gpid>/update', methods=['GET', 'POST'])
@login_required
def updateGP(seasonid, ageid, sasid, gpid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        gameNumber = request.form['gameNumber']
        tourNumber = request.form['tourNumber']
 
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
            GP        = GameProtocol()
            GP.GP_ID  = gpid

            # Заготовка для отслеживания только отличающихся значений полей при обновлении
            # GPfields  = GameProtocol._meta.fields
            # currentGP = GameProtocol.get(GP_ID = gpid)
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
                sasid    = sasid
            )
        )

### Удаление игрового протокола
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/<int:gpid>/delete', methods  = ['GET', 'POST'])
@login_required
def deleteGP(seasonid, ageid, sasid, gpid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            GameProtocol.get(GP_ID = gpid).delete_instance()

        return redirect(
            url_for('listGP',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )
