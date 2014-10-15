#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField

from Younoshi import *

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
