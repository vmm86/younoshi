#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField, ForeignKeyField

from DB import *

from City import City

## Спортивные школы
class School(DB):
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
                ('school_ID', 'city_ID'), True),)
