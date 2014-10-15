#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import IntegerField, PrimaryKeyField, DateField, ForeignKeyField

from DB import *

from Season   import Season
from Age      import Age
from Stage    import Stage
from GameType import GameType

## СезонВозрастСтадия
class SeasonAgeStage(DB):
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
        related_name = 'gameType_of_SAS',
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
                ('SAS_ID', 'season_ID', 'age_ID', 'stage_ID'), True),)
