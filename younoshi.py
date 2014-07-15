#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime, MySQLdb

from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import default_exceptions, HTTPException, NotFound

from flask import Flask, g, redirect, request, session, url_for, abort, render_template, flash
from functools import wraps
from hashlib import md5
from peewee import *

# Базовая конфигурация.
DB_NAME    = 'younoshi'
DB_USER    = 'root'
DB_PASSWD  = 'ckpvmm86'

USER       = 'test'
PASSWD     = 'test'

SECRET_KEY = '~a8a<uccng{,3}fr$[#n5\*s=h7"2n=}jhd-?y6dbb8a(n6+esykqy'
DEBUG      = True

# TRAP_BAD_REQUEST_ERRORS = True

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(__name__) # доступ к переменным базовой конфигурации в верхнем регистре
app.debug = True

# Создание экземпляра базы данных Peewee.
# Все модели будут использовать его для сохранения информции.
younoshi_db = MySQLDatabase(app.config['DB_NAME'], **{'passwd': app.config['DB_PASSWD'], 'user': app.config['DB_USER']})

# Определение модели - базового класса модели, который определяет, какую БД использовать.
# Все его подкласссы будут наследовать указанное в нём хранинище.
class YounoshiModel(Model):
    class Meta:
        database = younoshi_db

# Модели каждой таблицы в БД определяют их поля (столбцы) декларативно, в стиле Django.

## Пользователи
class User(YounoshiModel):
    user_ID      = PrimaryKeyField(db_column='user_ID')
    userName     = CharField(db_column='userName',max_length=128,null=False)
    userPassword = CharField(db_column='userPassword',max_length=128,null=False)

    class Meta:
        db_table = 'User'
        order_by = ('user_ID',)

## Города
class City(YounoshiModel):
    city_ID      = PrimaryKeyField(db_column='city_ID')
    cityName     = CharField(db_column='cityName',max_length=128,null=False)

    class Meta:
        db_table = 'City'
        order_by = ('city_ID',)

## Спортивные школы
class School(YounoshiModel):
    school_ID    = PrimaryKeyField(db_column='school_ID')
    city_ID      = ForeignKeyField(db_column='city_ID',rel_model=City,related_name='school_of_city',on_delete='NO ACTION',on_update='NO ACTION',to_field='city_ID',null=False)
    schoolName   = CharField(db_column='schoolName',max_length=128,null=False)

    class Meta:
        db_table = 'School'
        order_by = ('school_ID',)
        indexes  = (
            (('school_ID', 'city_ID'),True),
        )

## Возраста
class Age(YounoshiModel):
    age_ID       = PrimaryKeyField(db_column='age_ID')
    ageName      = IntegerField(db_column='ageName',null=False)

    class Meta:
        db_table = 'Age'
        order_by = ('age_ID',)

## Команды
class Team(YounoshiModel):
    team_ID      = PrimaryKeyField(db_column='team_ID')
    school_ID    = ForeignKeyField(db_column='school_ID',rel_model=School,related_name='team_of_school',on_delete='NO ACTION',on_update='NO ACTION',to_field='school_ID',null=False)
    age_ID       = ForeignKeyField(db_column='age_ID',rel_model=Age,related_name='age_of_team',on_delete='NO ACTION',on_update='NO ACTION',to_field='age_ID',null=False)
    teamName     = CharField(db_column='teamName',max_length=128,null=False)

    class Meta:
        db_table = 'Team'
        order_by = ('team_ID',)
        indexes  = (
            (('team_ID', 'school_ID', 'age_ID'),True),
        )

## Сезоны
class Season(YounoshiModel):
    season_ID    = PrimaryKeyField(db_column='season_ID')
    seasonName   = CharField(db_column='seasonName',max_length=128,null=False)

    class Meta:
        db_table = 'Season'
        order_by = ('season_ID',)

## Игровые стадии
class Stage(YounoshiModel):
    stage_ID     = PrimaryKeyField(db_column='stage_ID')
    stageType    = CharField(db_column='stageType',max_length=1,null=False)
    stageName    = CharField(db_column='stageName',max_length=128,null=False)

    class Meta:
        db_table = 'Stage'
        order_by = ('stage_ID',)

## СезонВозрастСтадия
class SeasonAgeStage(YounoshiModel):
    SAS_ID       = PrimaryKeyField(db_column='SAS_ID')
    season_ID    = ForeignKeyField(db_column='season_ID',rel_model=Season,related_name='season_of_SAS',on_delete='NO ACTION',on_update='NO ACTION',to_field='season_ID',null=False)
    age_ID       = ForeignKeyField(db_column='age_ID',rel_model=Age,related_name='age_of_SAS',on_delete='NO ACTION',on_update='NO ACTION',to_field='age_ID',null=False)
    stage_ID     = ForeignKeyField(db_column='stage_ID',rel_model=Stage,related_name='stage_of_SAS',on_delete='NO ACTION',on_update='NO ACTION',to_field='stage_ID',null=False)

    class Meta:
        db_table = 'SeasonAgeStage'
        order_by = ('SAS_ID',)
        indexes  = (
            (('SAS_ID', 'season_ID', 'age_ID', 'stage_ID'),True),
        )

## СезонВозрастСтадияКоманда
class SeasonAgeStageTeam(YounoshiModel):
    SAST_ID      = PrimaryKeyField(db_column='team_ID',)
    SAS_ID       = ForeignKeyField(db_column='SAS_ID',rel_model=SeasonAgeStage,related_name='season_of_SAS',on_delete='NO ACTION',on_update='NO ACTION',to_field='SAS_ID',null=False)
    team_ID      = ForeignKeyField(db_column='SAST_ID',rel_model=Team,related_name='stage_of_SAS',on_delete='NO ACTION',on_update='NO ACTION',to_field='team_ID',null=False)

    class Meta:
        db_table = 'SeasonAgeStageTeam'
        order_by = ('SAST_ID',)
        indexes  = (
            (('SAST_ID', 'SAS_ID', 'team_ID'),True),
        )

## Игровой протокол
class GameProtocol(YounoshiModel):
    GP_ID              = PrimaryKeyField(db_column='GP_ID')
    gameNumber         = CharField(db_column='gameNumber',max_length=16,null=True)
    tourNumber         = IntegerField(db_column='tourNumber',null=True)
    gameDate           = DateField(db_column='gameDate',formats='%Y-%m-%d',null=False)
    homeTeam_ID        = ForeignKeyField(db_column='homeTeam_ID',rel_model=SeasonAgeStageTeam,related_name='homeTeam_of_SAST',on_delete='NO ACTION',on_update='NO ACTION',to_field='SAS_ID',null=False)
    guestTeam_ID       = ForeignKeyField(db_column='guestTeam_ID', rel_model=SeasonAgeStageTeam,related_name='guestTeam_of_SAST',on_delete='NO ACTION',on_update='NO ACTION',to_field='SAS_ID',null=False)
    homeTeamScoreGame  = IntegerField(db_column='homeTeamScoreGame',null=False)
    guestTeamScoreGame = IntegerField(db_column='guestTeamScoreGame',null=False)
    homeTeamScore11m   = IntegerField(db_column='homeTeamScore11m',null=True)
    guestTeamScore11m  = IntegerField(db_column='guestTeamScore11m',null=True)
    is_Semifinal       = BooleanField(db_column='is_Semifinal',default=False,null=False)
    is_Final           = BooleanField(db_column='is_Final',default=False,null=False)

    class Meta:
        db_table       = 'GameProtocol'
        order_by       = ('GP_ID',)
        indexes        = (
            (('GP_ID', 'homeTeam_ID', 'guestTeam_ID'),True),
        )

# Авторизация
# def auth_user(user):
#     session['logged_in'] = True
#     session['user_ID']   = User.user_ID
#     session['userName']  = User.userName
#     flash('Вы вошли в систему как %s' % (user.userName))

# Получить данные о пользователе из сессии
# def get_current_user():
#     if session.get('logged_in'):
#         return User.get(User.id == session['user_ID'])

# Задаётся декоратор вида, указывающий пользователю, что он должен войти в систему для того, чтобы получить доступ к виду.
# Декоратор проверяет сессию, и если пользователь не вошёл в систему, он перенаправляется на вид login.
# def login_required(f):
#     @wraps(f)
#     def inner(*args, **kwargs):
#         if not session.get('logged_in'):
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return inner

# Получаем одиночный объект, соответствующий запросу или страницу ошибки 404.
# Используется алиас вызова метода "GET" из модели, который получает одиночный объект 
# или выдаёт исключение DoesNotExist, если ни одного такого объекта не найдено.
def get_object_or_404(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        abort(404)

# Сздание и удаление подключения к БД по каждому запросу.
# @app.before_request
# def before_request():
#     g.db = younoshi_db
#     g.db.connect()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

# Виды

## Главная страница
@app.route('/')
def mainpage():
    # # В зависимости от того, вошёл пользователь в систему или нет, ему показывается стартовая страница.
    # if session.get('logged_in'):
    #     return join()
    # else:
    #     return city()

    return render_template('index.html')

## Вход в систему
# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST' and request.form['loginForm']:
#         try:
#             user = User.get(
#                 userName=request.form['userName'],
#                 userPassword=md5(request.form['userPassword']).hexdigest()
#             )
#         except User.DoesNotExist:
#             flash('Пароль введён некорректно - попробуйте ещё раз')
#         else:
#             auth_user(user)
#             return redirect(url_for('homepage'))

#     return render_template('login.html')

## Выход из системы
# @app.route('/logout/')
# def logout():
#     session.pop('logged_in', None)
#     flash('Вы вышли из системы')
#     return redirect(url_for('homepage'))

# @app.errorhandler(400)
# def key_error(e):
#     flash('К сожалению, ваш запрос не удалось выполнить. Попробуйте сделать это ещё раз, введя все необходимые данные.')
#     return render_template('index.html'), 400

## Города
@app.route('/city')
def listCity():
    listCity = City.select().order_by(City.cityName)
    return render_template(
        'listCity.html', 
            listCity = listCity
    )

@app.route('/city/create', methods=['GET', 'POST'])
def createCity():
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            cityname  = request.form['cityName']
            City.create(cityName   = cityname)
            return redirect(
                url_for('listCity')
            )

@app.route('/city/<int:cityid>/update', methods = ['GET', 'POST'])
def updateCity(cityid):
    if request.method == 'POST':
        if  request.form['modify'] == 'update':
            cityname  = request.form['cityName']
            City.update(cityName   = cityname).where(City.city_ID == cityid).execute()
            return redirect(
                url_for('listCity')
            )

@app.route('/city/<int:cityid>/delete', methods = ['GET', 'POST'])
def deleteCity(cityid):
    if request.method == 'POST':
        if  request.form['modify'] == 'delete':
            try:
                City.get(city_ID   = cityid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот город, пока с ним связана хотя бы одна спортивная школа')
            return redirect(
                url_for('listCity')
            )

## Спортивные школы
@app.route('/city/<int:cityid>/school')
def listSchool(cityid):
    listCity   = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except City.DoesNotExist:
        cityname = 0
    listSchool = School.select().join(City).where(City.city_ID == cityid).order_by(School.schoolName)
    return render_template(
        'listSchool.html', 
            listCity   = listCity, 
            listSchool = listSchool, 
            cityid     = cityid, 
            cityname   = cityname
    )

@app.route('/city/<int:cityid>/school/create', methods = ['GET', 'POST'])
def createSchool(cityid):
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            schoolname = request.form['schoolName']
            School.create(city_ID  = cityid, schoolName  = schoolname)
            return redirect(
                url_for('listSchool', 
                    cityid = cityid)
            )

@app.route('/city/<int:cityid>/school/<int:schoolid>/update', methods = ['GET', 'POST'])
def updateSchool(cityid, schoolid):
    if request.method == 'POST':
        if  request.form['modify'] == 'update':
            schoolname = request.form['schoolName']
            School.update(city_ID  = cityid, schoolName  = schoolname).where(School.school_ID == schoolid).execute()
            return redirect(
                url_for('listSchool', 
                    cityid = cityid)
            )

@app.route('/city/<int:cityid>/school/<int:schoolid>/delete', methods = ['GET', 'POST'])
def deleteSchool(cityid, schoolid):
    if request.method == 'POST':
        if  request.form['modify'] == 'delete':
            try:
                School.get(city_ID = cityid, school_ID = schoolid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту спортивную школу, пока с ней связана хотя бы одна команда')
            return redirect(
                url_for('listSchool', 
                    cityid = cityid)
            )

## Команды
@app.route('/city/<int:cityid>/school/<int:schoolid>/team')
def listTeam(cityid, schoolid):
    listCity = City.select().order_by(City.cityName)
    try:
        cityname = City.get(city_ID = cityid).cityName
    except City.DoesNotExist:
        cityname   = None
    listSchool = School.select().join(City).where(City.city_ID == cityid).order_by(School.schoolName)
    try:
        schoolname = School.get(school_ID = schoolid).schoolName
    except School.DoesNotExist:
        schoolname = None
    listAge    = Age.select().order_by(Age.ageName)
    listTeam   = Team.select().join(School).where(School.school_ID == schoolid).join(City).where(City.city_ID == cityid).order_by(Team.team_ID)
    return render_template(
        'listTeam.html', 
            listCity   = listCity, 
            listSchool = listSchool, 
            listAge    = listAge, 
            listTeam   = listTeam, 
            cityid     = cityid, 
            cityname   = cityname, 
            schoolid   = schoolid, 
            schoolname = schoolname
    )

@app.route('/city/<int:cityid>/school/<int:schoolid>/team/create', methods = ['GET', 'POST'])
def createTeam(cityid, schoolid):
    if  request.form['modify'] == 'reset':
        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid)
            )
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            teamname  = request.form['teamName']
            ageid     = request.form['ageid']
            Team.create(school_ID  = schoolid,  age_ID = ageid,  teamName = teamname)
            return redirect(
                url_for('listTeam', 
                    cityid   = cityid, 
                    schoolid = schoolid)
            )

@app.route('/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/update', methods = ['GET', 'POST'])
def updateTeam(cityid, schoolid, teamid):
    if  request.form['modify'] == 'cancel':
        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid)
        )
    if request.method == 'POST':
        if  request.form['modify'] == 'update':
            teamname  = request.form['teamName']
            ageid     = request.form['ageid']
            Team.update(school_ID  = schoolid,  age_ID = ageid,  teamName = teamname).where(Team.team_ID == teamid).execute()
            return redirect(
                url_for('listTeam', 
                    cityid   = cityid, 
                    schoolid = schoolid,
                    teamid   = teamid)
            )

@app.route('/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/delete', methods  = ['GET', 'POST'])
def deleteTeam(cityid, schoolid, teamid):
    if request.method == 'POST':
        if  request.form['modify'] == 'delete':
            Team.get(school_ID     = schoolid, team_ID = teamid).delete_instance()
            return redirect(
                url_for('listTeam', 
                    cityid   = cityid, 
                    schoolid = schoolid,
                    teamid   = teamid)
            )

## Игровые стадии
@app.route('/stage')
def listStage():
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)
    return render_template(
        'listStage.html', 
            listStage = listStage
    )

@app.route('/stage/create', methods=['GET', 'POST'])
def createStage():
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            stagetype  = request.form['stagetype']
            stagename  = request.form['stageName']
            Stage.create(stageType = stagetype, stageName = stagename)
            return redirect(
                url_for('listStage')
            )

@app.route('/stage/<int:stageid>/update', methods = ['GET', 'POST'])
def updateStage(stageid):
    if request.method == 'POST':
        if  request.form['modify'] == 'update':
            stagetype  = request.form['stagetype']
            stagename  = request.form['stageName']
            Stage.update(stageType = stagetype, stageName = stagename).where(Stage.stage_ID == stageid).execute()
            return redirect(
                url_for('listStage')
            )

@app.route('/stage/<int:stageid>/delete', methods = ['GET', 'POST'])
def deleteStage(stageid):
    if request.method == 'POST':
        if  request.form['modify'] == 'delete':
            try:
                Stage.get(stage_ID = stageid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту игровую стадию, пока с ним связан хотя бы один внутрисезонный игровой этап')
            return redirect(
                url_for('listStage')
            )

## Сезоны
@app.route('/season')
def listSeason():
    listSeason = Season.select().order_by(Season.seasonName)
    return render_template(
        'listSeason.html', 
            listSeason = listSeason
    )

@app.route('/season/create', methods=['GET', 'POST'])
def createSeason():
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            seasonname  = request.form['seasonName']
            Season.create(seasonName = seasonname)
            return redirect(
                url_for('listSeason')
            )

@app.route('/season/<int:seasonid>/update', methods = ['GET', 'POST'])
def updateSeason(seasonid):
    if request.method == 'POST':
        if  request.form['modify'] == 'update':
            seasonname  = request.form['seasonName']
            Season.update(seasonName = seasonname).where(Season.season_ID == seasonid).execute()
            return redirect(
                url_for('listSeason')
            )

@app.route('/season/<int:seasonid>/delete', methods = ['GET', 'POST'])
def deleteSeason(seasonid):
    if request.method == 'POST':
        if  request.form['modify'] == 'delete':
            try:
                Season.get(season_ID = seasonid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить этот сезон, пока с ним связан хотя бы один внутрисезонный игровой этап')
            return redirect(
                url_for('listSeason')
            )

## СезонВозрастСтадия
@app.route('/season/<int:seasonid>/sas')
def listSAS(seasonid):
    listSeason = Season.select().order_by(Season.season_ID.asc())
    try:
        seasonname = Season.get(season_ID = seasonid).seasonName
    except Season.DoesNotExist:
        seasoname  = None
    listAge   = Age.select().order_by(Age.ageName)
    listStage = Stage.select().order_by(Stage.stageType, Stage.stageName)
    listSAS   = SeasonAgeStage.select().order_by(SeasonAgeStage.SAS_ID)
    return render_template(
        'SAS.html', 
            listSeason = listSeason,
            listAge    = listAge,
            listStage  = listStage,
            listSAS    = listSAS,
            seasonid   = seasonid
    )

@app.route('/sas/create', methods=['GET', 'POST'])
def createSAS():
    if request.method == 'POST':
        if  request.form['modify'] == 'create':
            seasonid  = request.form['season_ID']
            ageid     = request.form['age_ID']
            stageid   = request.form['stage_ID']
            SeasonAgeStage.create(season_ID = seasonid, age_ID = ageid, stage_ID = stageid)
            return redirect(
                url_for('listSAS')
            )
