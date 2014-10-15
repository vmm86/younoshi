#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, ForeignKeyField

from Younoshi import *

from SAS   import SeasonAgeStage
from Team  import Team
from Stage import Stage

## СезонВозрастСтадияКоманда
class SeasonAgeStageTeam(Younoshi):
    SAST_ID = PrimaryKeyField(
        db_column = 'SAST_ID')
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
                ('SAST_ID', 'SAS_ID', 'team_ID'), True),)
