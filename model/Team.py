#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField, ForeignKeyField

from connect import *

from School import School
from Age    import Age

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
                ('team_ID', 'school_ID', 'age_ID'), True),)
