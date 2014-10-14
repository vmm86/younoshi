#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField

from connect import *

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
