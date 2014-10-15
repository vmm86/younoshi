#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import IntegerField, PrimaryKeyField, DateField, BooleanField, ForeignKeyField

from DB import *

from SAST import SeasonAgeStageTeam

## Игровой протокол
class GameProtocol(DB):
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
