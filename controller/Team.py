#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import session, render_template, url_for, request, redirect, flash

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import City, School, Team, Age

from User import login_required

## Команды
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
        listTeam   = listTeam)

### Добавление команд
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
                teamName = teamname)

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid))

### Изменение команд
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
                teamid   = teamid))

### Удаление команд
@login_required
def deleteTeam(cityid, schoolid, teamid):
    if request.method == 'POST' and request.form['modify'] == 'delete':

        if session['demo']:
            pass
        else:
            # Ограничение по внешнему ключу FK_SAST_Team 
            # не позволяет удалить команду при наличии связанных с ней игровых этапов.
            try:
                Team.get(school_ID = schoolid, team_ID = teamid).delete_instance()
            except IntegrityError:
                flash('Вы не можете удалить эту команду, пока она добавлена хотя бы в один игровой этап', 'danger')

        return redirect(
            url_for('listTeam', 
                cityid   = cityid, 
                schoolid = schoolid,
                teamid   = teamid))
