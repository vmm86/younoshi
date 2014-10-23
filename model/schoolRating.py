#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, IntegerField, CharField

from DB import *

## Рейтинг команд
class schoolRating(DB):
    season_ID  = IntegerField(
        db_column = 'season_ID')
    seasonName = CharField(
        db_column  = 'seasonName',
        max_length = 128)
    city_ID    = IntegerField(
        db_column = 'city_ID')
    cityName   = CharField(
        db_column  = 'cityName',
        max_length = 128)
    school_ID = PrimaryKeyField(
        db_column = 'school_ID')
    schoolName = CharField(
        db_column  = 'schoolName',
        max_length = 128)

    games       = IntegerField(
        db_column = 'games')
    wins        = IntegerField(
        db_column = 'wins')
    equals      = IntegerField(
        db_column = 'equals')
    scored      = IntegerField(
        db_column = 'scored')
    missed      = IntegerField(
        db_column = 'missed')
    goals       = IntegerField(
        db_column = 'goals')
    playoff     = IntegerField(
        db_column = 'playoff')
    playoff_11m = IntegerField(
        db_column = 'playoff_11m')
    playoff_SF  = IntegerField(
        db_column = 'playoff_SF')
    playoff_F   = IntegerField(
        db_column = 'playoff_F')

    schoolRating  = IntegerField(
        db_column = 'schoolRating')

    class Meta:
        db_table = 'schoolRating'
        order_by = ('-schoolRating',)
