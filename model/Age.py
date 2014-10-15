#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, IntegerField

from DB import *

## Возраста
class Age(DB):
    age_ID = PrimaryKeyField(
        db_column = 'age_ID')
    ageName = IntegerField(
        db_column = 'ageName',
        null      = False)

    class Meta:
        db_table = 'Age'
        order_by = ('age_ID',)
