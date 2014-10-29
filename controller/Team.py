#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import DoesNotExist, IntegrityError

from model import City, School, Team, Age

from User import login_required

# Команды
@login_required
def listTeam(cityid, schoolid):
    # Список городов и их дочерних школ, название текущего города и школы
    listCity   = City.select().order_by(City.cityName)
    listSchool = School.select().join(City).where(City.city_ID == cityid).order_by(School.schoolName)
    try:
        cityname   = City.get(city_ID = cityid).cityName
        schoolname = School.get(school_ID = schoolid).schoolName
    except DoesNotExist:
        cityname   = None
        schoolname = None

    # Список команд в выбранной школе
    listTeam = Team.select().join(School).where(School.school_ID == schoolid).join(City).where(City.city_ID == cityid).order_by(Team.teamName)
    # Список возрастов
    listAge  = Age.select().order_by(Age.ageName)

    # Переменные для автозаполнения модальной формы добавления/обновления данных в JS-скрипте шаблона
    ## Список полей
    modifyFields = ['teamName', 'age_ID', 'ageName']
    ## Список групп радиокнопок
    modifyRadios = ['age_ID']
    ## Заголовки модального окна
    createHeader = ['"Создать новую юношескую команду"']
    updateHeader = ['"Изменить "', 'teamName', '" (возраст "', 'ageName', '")"']
    ## Действия формы
    createAction = ['"/city/"', cityid, '"/school/"', schoolid, '"/team/create"']
    updateAction = ['"/city/"', cityid, '"/school/"', schoolid, '"/team/"', 'PK_ID', '"/update"']
    deleteAction = ['"/city/"', cityid, '"/school/"', schoolid, '"/team/"', 'PK_ID', '"/delete"']

    # Вывод шаблона
    return render_template(
        'Team.jinja.html', 
        listCity     = listCity, 
        cityid       = cityid, 
        cityname     = cityname, 
        listSchool   = listSchool, 
        schoolid     = schoolid, 
        schoolname   = schoolname,
        listTeam     = listTeam,
        listAge      = listAge, 
        modifyFields = modifyFields,
        modifyRadios = modifyRadios,
        createHeader = createHeader,
        updateHeader = updateHeader,
        createAction = createAction,
        updateAction = updateAction,
        deleteAction = deleteAction)

### Добавление команд
@login_required
def createTeam(cityid, schoolid):
    # Получение полей формы из шаблона
    teamname = request.form['teamName']
    ageid    = request.form['age_ID']

    # Сохранение новой записи в БД
    if session['demo']:
        pass
    else:
        Team.create(
            school_ID = schoolid, 
            age_ID = ageid, 
            teamName = teamname)

    # Редирект на вид list
    return redirect(
        url_for('listTeam', 
            cityid   = cityid, 
            schoolid = schoolid))

### Изменение команд
@login_required
def updateTeam(cityid, schoolid, teamid):
    # Получение полей формы из шаблона
    teamname = request.form['teamName']
    ageid    = request.form['age_ID']

    # Обновление текущей записи в БД
    if session['demo']:
        pass
    else:
        team           = Team()
        team.team_ID   = teamid
        team.school_ID = schoolid
        team.age_ID    = ageid
        team.teamName  = teamname
        team.save()

    # Редирект на вид list
    return redirect(
        url_for('listTeam', 
            cityid   = cityid, 
            schoolid = schoolid,
            teamid   = teamid))

### Удаление команд
@login_required
def deleteTeam(cityid, schoolid, teamid):
    # Удаление текущей записи в БД
    if session['demo']:
        pass
    else:
        # Ограничение по внешнему ключу FK_SAST_Team 
        # не позволяет удалить команду при наличии связанных с ней игровых этапов.
        try:
            Team.get(school_ID = schoolid, team_ID = teamid).delete_instance()
        except IntegrityError:
            flash('Вы не можете удалить эту команду, пока она добавлена хотя бы в один игровой этап', 'danger')

    # Редирект на вид list
    return redirect(
        url_for('listTeam', 
            cityid   = cityid, 
            schoolid = schoolid,
            teamid   = teamid))
