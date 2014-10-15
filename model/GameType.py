#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField

from DB import *

## Типы соревнований
class GameType(DB):
    gameType_ID = PrimaryKeyField(
        db_column = 'gameType_ID')
    gameTypeName = CharField(
        db_column  = 'gameTypeName',
        max_length = 16,
        null       = False)

    class Meta:
        db_table = 'GameType'
        order_by = ('gameType_ID',)
