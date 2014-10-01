#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime, MySQLdb

from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import default_exceptions, HTTPException, NotFound

from flask import Flask, g, redirect, request, session, url_for, abort, render_template, flash, jsonify
from jinja2 import TemplateNotFound
import json
from functools import wraps
from hashlib import md5
from peewee import *

# Базовая конфигурация.
DB_NAME    = 'younoshi'
DB_USER    = 'root'
DB_PASSWD  = 'ckpvmm86'

SECRET_KEY = '~a8a<uccng{,3}fr$[#n5\*s=h7"2n=}jhd-?y6dbb8a(n6+esykqy'
DEBUG      = True

# TRAP_BAD_REQUEST_ERRORS = True

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(__name__) # доступ к переменным базовой конфигурации в верхнем регистре

# Создание экземпляра базы данных Peewee.
# Все модели будут использовать его для сохранения информции.
younoshi_db = MySQLDatabase(app.config['DB_NAME'], **{'passwd': app.config['DB_PASSWD'], 'user': app.config['DB_USER']})

# Определение модели - базового класса модели, который определяет, какую БД использовать.
# Все его подкласссы будут наследовать указанное в нём хранинище.
class Younoshi(Model):
    class Meta:
        database = younoshi_db

# Модели каждой таблицы в БД определяют их поля (столбцы) декларативно, в стиле Django.

## Пользователи
class User(Younoshi):
    user_ID = PrimaryKeyField(
        db_column = 'user_ID'
    )
    userLogin = CharField(
        db_column  = 'userLogin',
        max_length = 32,
        null       = False
    )
    userPassword = CharField(
        db_column  = 'userPassword',
        max_length = 32,
        null       = False
    )
    userName = CharField(
        db_column  = 'userName',
        max_length = 32,
        null       = False
    )

    class Meta:
        db_table = 'User'
        order_by = ('user_ID',)

## Города
class City(Younoshi):
    city_ID = PrimaryKeyField(
        db_column = 'city_ID'
    )
    cityName = CharField(
        db_column  = 'cityName',
        max_length = 128,
        null       = False
    )

    class Meta:
        db_table = 'City'
        order_by = ('city_ID',)

## Спортивные школы
class School(Younoshi):
    school_ID = PrimaryKeyField(
        db_column = 'school_ID'
    )
    city_ID = ForeignKeyField(
        db_column    = 'city_ID',
        rel_model    = City,
        related_name = 'school_of_city',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'city_ID',
        null         = False
    )
    schoolName = CharField(
        db_column  = 'schoolName',
        max_length = 128,
        null       = False
    )

    class Meta:
        db_table = 'School'
        order_by = ('school_ID',)
        indexes  = (
            (
                ('school_ID', 'city_ID'),
                True
            ),
        )

## Возраста
class Age(Younoshi):
    age_ID = PrimaryKeyField(
        db_column = 'age_ID'
    )
    ageName = IntegerField(
        db_column = 'ageName',
        null      = False
    )

    class Meta:
        db_table = 'Age'
        order_by = ('age_ID',)

## Команды
class Team(Younoshi):
    team_ID = PrimaryKeyField(
        db_column = 'team_ID'
    )
    school_ID = ForeignKeyField(
        db_column    = 'school_ID',
        rel_model    = School,
        related_name = 'team_of_school',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'school_ID',
        null         = False
    )
    age_ID = ForeignKeyField(
        db_column    = 'age_ID',
        rel_model    = Age,
        related_name = 'age_of_team',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'age_ID',
        null         = False
    )
    teamName = CharField(
        db_column  = 'teamName',
        max_length = 128,
        null       = False
    )

    class Meta:
        db_table = 'Team'
        order_by = ('team_ID',)
        indexes  = (
            (
                ('team_ID', 'school_ID', 'age_ID'),
                True
            ),
        )

## Сезоны
class Season(Younoshi):
    season_ID = PrimaryKeyField(
        db_column = 'season_ID'
    )
    seasonName = CharField(
        db_column  = 'seasonName',
        max_length = 128,
        null       = False
    )

    class Meta:
        db_table = 'Season'
        order_by = ('season_ID',)

## Игровые стадии
class Stage(Younoshi):
    stage_ID = PrimaryKeyField(
        db_column = 'stage_ID'
    )
    stageType = CharField(
        db_column  = 'stageType',
        max_length = 1,
        null       = False
    )
    stageName = CharField(
        db_column  = 'stageName',
        max_length = 128,
        null       = False
    )

    class Meta:
        db_table = 'Stage'
        order_by = ('stage_ID',)

## Типы соревнований
class GameType(Younoshi):
    gameType_ID = PrimaryKeyField(
        db_column = 'gameType_ID'
    )
    gameTypeName = CharField(
        db_column  = 'gameTypeName',
        max_length = 16,
        null       = False
    )

    class Meta:
        db_table = 'GameType'
        order_by = ('gameType_ID',)

## СезонВозрастСтадия
class SeasonAgeStage(Younoshi):
    SAS_ID = PrimaryKeyField(
        db_column = 'SAS_ID'
    )
    season_ID = ForeignKeyField(
        db_column    = 'season_ID',
        rel_model    = Season,
        related_name = 'season_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'season_ID',
        null         = False
    )
    age_ID = ForeignKeyField(
        db_column    = 'age_ID',
        rel_model    = Age,
        related_name = 'age_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'age_ID',
        null         = False
    )
    stage_ID = ForeignKeyField(
        db_column    = 'stage_ID',
        rel_model    = Stage,
        related_name = 'stage_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'stage_ID',
        null         = False
    )
    gameType_ID = ForeignKeyField(
        db_column    = 'gameType_ID',
        rel_model    = GameType,
        related_name = 'gameTitle_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'gameType_ID'
    )
    startDate = DateField(
        db_column = 'startDate',
        formats   = '%Y-%m-%d',
        null      = True
    )
    finishDate = DateField(
        db_column = 'finishDate',
        formats   = '%Y-%m-%d',
        null      = True
    )

    class Meta:
        db_table = 'SeasonAgeStage'
        order_by = ('SAS_ID',)
        indexes  = (
            (
                ('SAS_ID', 'season_ID', 'age_ID', 'stage_ID'),
                True
            ),
        )

## СезонВозрастСтадияКоманда
class SeasonAgeStageTeam(Younoshi):
    SAST_ID = PrimaryKeyField(
        db_column='SAST_ID'
    )
    SAS_ID = ForeignKeyField(
        db_column    = 'SAS_ID',
        rel_model    = SeasonAgeStage,
        related_name = 'SAS_of_SAST',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'SAS_ID',
        null         = False
    )
    team_ID = ForeignKeyField(
        db_column    = 'team_ID',
        rel_model    = Team,
        related_name = 'team_of_SAST',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False
    )
    substage_ID = ForeignKeyField(
        db_column    = 'substage_ID',
        rel_model    = Stage,
        related_name = 'substage_of_SAST',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'stage_ID',
        null         = True
    )

    class Meta:
        db_table = 'SeasonAgeStageTeam'
        order_by = ('SAST_ID',)
        indexes  = (
            (
                ('SAST_ID', 'SAS_ID', 'team_ID'),
                True
            ),
        )

## Игровой протокол
class GameProtocol(Younoshi):
    GP_ID = PrimaryKeyField(
        db_column = 'GP_ID'
    )
    gameNumber = IntegerField(
        db_column  = 'gameNumber',
        null       = True
    )
    tourNumber = IntegerField(
        db_column = 'tourNumber',
        null      = True
    )
    stageNumber = IntegerField(
        db_column = 'stageNumber',
        null      = True
    )
    gameDate = DateField(
        db_column = 'gameDate',
        formats   = '%Y-%m-%d',
        null      = False
    )
    homeTeam_ID = ForeignKeyField(
        db_column    = 'homeTeam_ID',
        rel_model    = SeasonAgeStageTeam,
        related_name = 'homeTeam_of_GP',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False
    )
    guestTeam_ID = ForeignKeyField(
        db_column    = 'guestTeam_ID',
        rel_model    = SeasonAgeStageTeam,
        related_name = 'guestTeam_of_GP',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False
    )
    homeTeamScoreGame = IntegerField(
        db_column = 'homeTeamScoreGame',
        null      = True
    )
    guestTeamScoreGame = IntegerField(
        db_column = 'guestTeamScoreGame',
        null      = True
    )
    homeTeamScore11m = IntegerField(
        db_column = 'homeTeamScore11m',
        null      = True
    )
    guestTeamScore11m = IntegerField(
        db_column = 'guestTeamScore11m',
        null      = True
    )
    is_Semifinal = BooleanField(
        db_column = 'is_Semifinal',
        default   = False,
        null      = False
    )
    is_Final = BooleanField(
        db_column = 'is_Final',
        default   = False,
        null      = False
    )

    class Meta:
        db_table = 'GameProtocol'
        order_by = ('GP_ID',)
        indexes  = (
            (
                ('GP_ID', 'homeTeam_ID', 'guestTeam_ID'),
                True
            ),
        )

# Создание и удаление подключения к БД по каждому запросу.
# @app.before_request
# def before_request():
#     g.db = younoshi_db
#     g.db.connect()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

# Получаем одиночный объект, соответствующий запросу или страницу ошибки 404.
# Используется алиас вызова метода "GET" из модели, который получает одиночный объект 
# или выдаёт исключение DoesNotExist, если ни одного такого объекта не найдено.
def get_object_or_404(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        abort(404)
        return render_template('404.jinja.html')

## Обработка ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        '404.jinja.html'
    ), 404

# @app.errorhandler(400)
# def key_error(e):
#     flash('К сожалению, ваш запрос не удалось выполнить. Попробуйте сделать это ещё раз, введя все необходимые данные.', 'danger')
#     return render_template('index.html'), 400

# Авторизация
def auth_user(user):
    session['logged_in'] = True
    session['user_ID']   = user.user_ID
    session['userLogin'] = user.userLogin
    if session['userLogin'] == 'demo':
        session['demo'] = True
    else:
        session['demo'] = None
    session['userName']  = user.userName
    flash('Вы успешно вошли в систему как %s' % (user.userName), 'success')

# Декоратор проверяет сессию, и если пользователь не вошёл в систему, он перенаправляется на вид login.
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(
                url_for('login')
            )
        return f(*args, **kwargs)
    return inner

# Виды

## Главная страница
@app.route('/')
def index():
    ### В зависимости от того, вошёл пользователь в систему или нет, ему показывается стартовая страница.
    if session.get('logged_in'):
        return render_template(
            'index.jinja.html'
        )
    else:
        return redirect(
            url_for('login')
        )

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
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы', 'warning')
    return redirect(
        url_for('index')
    )

## Города
@app.route('/city')
def listCity():
    listCity = City.select(City, fn.Count(School.city_ID).alias('countSchools')).join(School, JOIN_LEFT_OUTER).group_by(City).order_by(City.cityName)

    return render_template(
        'City.jinja.html', 
        listCity = listCity
    )

### Добавление городов
@app.route('/city/create', methods=['GET', 'POST'])
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

### Удаленеи команд
@app.route('/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/delete', methods = ['GET', 'POST'])
def deleteTeam(cityid, schoolid, teamid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            Team.get(school_ID = schoolid, team_ID = teamid).delete_instance()

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid,
                teamid   = teamid
            )
        )

## Стадии
@app.route('/stage')
def listStage():
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)

    return render_template(
        'Stage.jinja.html', 
        listStage = listStage
    )

### Добавление стадий
@app.route('/stage/create', methods = ['GET', 'POST'])
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
def listSeason():
    listSeason = Season.select().order_by(Season.seasonName)

    return render_template(
        'Season.jinja.html', 
        listSeason = listSeason
    )

### Добавление сезонов
@app.route('/season/create', methods = ['GET', 'POST'])
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
    listSAS      = SeasonAgeStage.select(SeasonAgeStage, fn.Count(SeasonAgeStageTeam.SAS_ID).alias('countSAST')).where(SeasonAgeStage.season_ID == seasonid, SeasonAgeStage.age_ID == ageid).join(SeasonAgeStageTeam, JOIN_LEFT_OUTER).switch(SeasonAgeStage).join(Stage).group_by(SeasonAgeStage).order_by(Stage.stageName, SeasonAgeStage.gameType_ID)

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
def createSAS(seasonid, ageid):
    if request.method == 'POST' and request.form['modify'] == 'create':
        stageid  = request.form['stage']
        gametype = request.form['gameType']

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
                    gameType_ID = gametype
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
def updateSAS(seasonid, ageid, sasid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        stageid  = request.form['stage']
        gametype = request.form['gameType']

        if session['demo']:
            pass
        else:
            SAS             = SeasonAgeStage()
            SAS.SAS_ID      = sasid
            SAS.season_ID   = seasonid
            SAS.age_ID      = ageid
            SAS.stage_ID    = stageid
            SAS.gameType_ID = gametype
            SAS.save()

        return redirect(
            url_for('listSAS',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )

### Удаление игровых этапов
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/delete', methods  = ['GET', 'POST'])
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
                ageid    = ageid,
                sasid    = sasid
            )
        )

## Команды в игровых этапах
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team')
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

    sastsubstagecount = SeasonAgeStageTeam.select().where(SeasonAgeStageTeam.SAS_ID == sasid).join(Stage, JOIN_LEFT_OUTER).where(Stage.stage_ID != None).count()

    return render_template(
        'SAST.jinja.html', 
        listSeason        = listSeason,
        seasonid          = seasonid,
        seasonname        = seasonname,
        listAge           = listAge,
        ageid             = ageid,
        agename           = agename,
        listSAS_Z         = listSAS_Z,
        listSAS_G         = listSAS_G,
        listSAS_P         = listSAS_P,
        sasid             = sasid,
        sastype           = sastype,
        filterCity        = filterCity,
        filterSchool      = filterSchool,
        filterTeam        = filterTeam,
        listSAST          = listSAST,
        listStage         = listStage,
        sastsubstagecount = sastsubstagecount
    )

### Добавление команд в игровые этапы
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/create', methods=['GET', 'POST'])
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
def deleteSAST(seasonid, ageid, sasid, sastid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            SeasonAgeStageTeam.get(SAST_ID = sastid).delete_instance()

        return redirect(
            url_for('listSAST',
                seasonid = seasonid,
                ageid    = ageid,
                sasid    = sasid
            )
        )

## Игровые протоколы
@app.route('/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp')
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

    gnmax = int(GameProtocol.select(fn.Max(GameProtocol.gameNumber)).scalar())
    gnmax += 1
    tnmax = int(GameProtocol.select(fn.Max(GameProtocol.tourNumber)).scalar())
    dmax  = GameProtocol.select(fn.Max(GameProtocol.gameDate)).scalar()

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

        gamedate = request.form['gameDate']
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
def updateGP(seasonid, ageid, sasid, gpid):
    if request.method == 'POST' and request.form['modify'] == 'update':
        gamenumber = request.form['gameNumber']
        tournumber = request.form['tourNumber']
 
        try:
            stagenumber = request.form['stageNumber']
        except KeyError:
            stagenumber = None
        if stagenumber == '':
            stagenumber = None

        gamedate = request.form['gameDate']
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
            GP                    = GameProtocol()
            GP.GP_ID              = gpid
            GP.gameNumber         = gamenumber
            GP.tourNumber         = tournumber
            GP.stageNumber        = stagenumber
            GP.gameDate           = gamedate
            GP.homeTeam_ID        = htid
            GP.guestTeam_ID       = gtid
            GP.homeTeamScoreGame  = htscoregame
            GP.guestTeamScoreGame = gtscoregame
            GP.homeTeamScore11m   = htscore11m
            GP.guestTeamScore11m  = gtscore11m
            GP.is_Semifinal       = issemifinal
            GP.is_Final           = isfinal
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
