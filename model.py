#! /usr/bin/python
# -*- coding: utf-8 -*-

import config

import MySQLdb

from peewee import *

dbname   = config.DB_NAME
dbpasswd = config.DB_PASSWD
dbuser   = config.DB_USER

# Создание экземпляра базы данных Peewee.
# Все модели будут использовать его для сохранения информции.
younoshi_db = MySQLDatabase(dbname, passwd = dbpasswd, user = dbuser)

# Создание и удаление подключения к БД по каждому запросу.

# from flask import g

# @app.before_request
# def before_request():
#     g.db = younoshi_db
#     g.db.connect()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

# Определение модели - базового класса модели, который определяет, какую БД использовать.
# Все его подкласссы будут наследовать указанное в нём хранинище.
class Younoshi(Model):
    class Meta:
        database = younoshi_db

# Модели каждой таблицы в БД определяют их поля (столбцы) декларативно, в стиле Django.

## Пользователи
class User(Younoshi):
    user_ID = PrimaryKeyField(
        db_column = 'user_ID')
    userLogin = CharField(
        db_column  = 'userLogin',
        max_length = 32,
        null       = False)
    userPassword = CharField(
        db_column  = 'userPassword',
        max_length = 32,
        null       = False)
    userName = CharField(
        db_column  = 'userName',
        max_length = 32,
        null       = False)

    class Meta:
        db_table = 'User'
        order_by = ('user_ID',)

## Города
class City(Younoshi):
    city_ID = PrimaryKeyField(
        db_column = 'city_ID')
    cityName = CharField(
        db_column  = 'cityName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'City'
        order_by = ('city_ID',)

## Спортивные школы
class School(Younoshi):
    school_ID = PrimaryKeyField(
        db_column = 'school_ID')
    city_ID = ForeignKeyField(
        db_column    = 'city_ID',
        rel_model    = City,
        related_name = 'school_of_city',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'city_ID',
        null         = False)
    schoolName = CharField(
        db_column  = 'schoolName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'School'
        order_by = ('school_ID',)
        indexes  = (
            (
                ('school_ID', 'city_ID'),
                True),)

## Возраста
class Age(Younoshi):
    age_ID = PrimaryKeyField(
        db_column = 'age_ID'
    )
    ageName = IntegerField(
        db_column = 'ageName',
        null      = False)

    class Meta:
        db_table = 'Age'
        order_by = ('age_ID',)

## Команды
class Team(Younoshi):
    team_ID = PrimaryKeyField(
        db_column = 'team_ID')
    school_ID = ForeignKeyField(
        db_column    = 'school_ID',
        rel_model    = School,
        related_name = 'team_of_school',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'school_ID',
        null         = False)
    age_ID = ForeignKeyField(
        db_column    = 'age_ID',
        rel_model    = Age,
        related_name = 'age_of_team',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'age_ID',
        null         = False)
    teamName = CharField(
        db_column  = 'teamName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'Team'
        order_by = ('team_ID',)
        indexes  = (
            (
                ('team_ID', 'school_ID', 'age_ID'),
                True),)

## Сезоны
class Season(Younoshi):
    season_ID = PrimaryKeyField(
        db_column = 'season_ID')
    seasonName = CharField(
        db_column  = 'seasonName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'Season'
        order_by = ('season_ID',)

## Игровые стадии
class Stage(Younoshi):
    stage_ID = PrimaryKeyField(
        db_column = 'stage_ID')
    stageType = CharField(
        db_column  = 'stageType',
        max_length = 1,
        null       = False)
    stageName = CharField(
        db_column  = 'stageName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'Stage'
        order_by = ('stage_ID',)

## Типы соревнований
class GameType(Younoshi):
    gameType_ID = PrimaryKeyField(
        db_column = 'gameType_ID')
    gameTypeName = CharField(
        db_column  = 'gameTypeName',
        max_length = 16,
        null       = False)

    class Meta:
        db_table = 'GameType'
        order_by = ('gameType_ID',)

## СезонВозрастСтадия
class SeasonAgeStage(Younoshi):
    SAS_ID = PrimaryKeyField(
        db_column = 'SAS_ID')
    season_ID = ForeignKeyField(
        db_column    = 'season_ID',
        rel_model    = Season,
        related_name = 'season_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'season_ID',
        null         = False)
    age_ID = ForeignKeyField(
        db_column    = 'age_ID',
        rel_model    = Age,
        related_name = 'age_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'age_ID',
        null         = False)
    stage_ID = ForeignKeyField(
        db_column    = 'stage_ID',
        rel_model    = Stage,
        related_name = 'stage_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'stage_ID',
        null         = False)
    gameType_ID = ForeignKeyField(
        db_column    = 'gameType_ID',
        rel_model    = GameType,
        related_name = 'gameTitle_of_SAS',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'gameType_ID')
    startDate = DateField(
        db_column = 'startDate',
        formats   = '%Y-%m-%d',
        null      = True )
    finishDate = DateField(
        db_column = 'finishDate',
        formats   = '%Y-%m-%d',
        null      = True)

    class Meta:
        db_table = 'SeasonAgeStage'
        order_by = ('SAS_ID',)
        indexes  = (
            (
                ('SAS_ID', 'season_ID', 'age_ID', 'stage_ID'),
                True),)

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
        null         = False)
    team_ID = ForeignKeyField(
        db_column    = 'team_ID',
        rel_model    = Team,
        related_name = 'team_of_SAST',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False)
    substage_ID = ForeignKeyField(
        db_column    = 'substage_ID',
        rel_model    = Stage,
        related_name = 'substage_of_SAST',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'stage_ID',
        null         = True)

    class Meta:
        db_table = 'SeasonAgeStageTeam'
        order_by = ('SAST_ID',)
        indexes  = (
            (
                ('SAST_ID', 'SAS_ID', 'team_ID'),
                True),)

## Игровой протокол
class GameProtocol(Younoshi):
    GP_ID = PrimaryKeyField(
        db_column = 'GP_ID')
    gameNumber = IntegerField(
        db_column  = 'gameNumber',
        null       = True)
    tourNumber = IntegerField(
        db_column = 'tourNumber',
        null      = True)
    stageNumber = IntegerField(
        db_column = 'stageNumber',
        null      = True)
    gameDate = DateField(
        db_column = 'gameDate',
        formats   = '%Y-%m-%d',
        null      = False)
    homeTeam_ID = ForeignKeyField(
        db_column    = 'homeTeam_ID',
        rel_model    = SeasonAgeStageTeam,
        related_name = 'homeTeam_of_GP',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False)
    guestTeam_ID = ForeignKeyField(
        db_column    = 'guestTeam_ID',
        rel_model    = SeasonAgeStageTeam,
        related_name = 'guestTeam_of_GP',
        on_delete    = 'NO ACTION',
        on_update    = 'NO ACTION',
        to_field     = 'team_ID',
        null         = False)
    homeTeamScoreGame = IntegerField(
        db_column = 'homeTeamScoreGame',
        null      = True)
    guestTeamScoreGame = IntegerField(
        db_column = 'guestTeamScoreGame',
        null      = True)
    homeTeamScore11m = IntegerField(
        db_column = 'homeTeamScore11m',
        null      = True)
    guestTeamScore11m = IntegerField(
        db_column = 'guestTeamScore11m',
        null      = True)
    is_Semifinal = BooleanField(
        db_column = 'is_Semifinal',
        default   = False,
        null      = False)
    is_Final = BooleanField(
        db_column = 'is_Final',
        default   = False,
        null      = False)

    class Meta:
        db_table = 'GameProtocol'
        order_by = ('GP_ID',)
        indexes  = (
            (
                ('GP_ID', 'homeTeam_ID', 'guestTeam_ID'),
                True),)
