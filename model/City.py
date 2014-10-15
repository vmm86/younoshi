#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField

from DB import *

## Города
class City(DB):
    city_ID = PrimaryKeyField(
        db_column = 'city_ID')
    cityName = CharField(
        db_column  = 'cityName',
        max_length = 128,
        null       = False)

    class Meta:
        db_table = 'City'
        order_by = ('city_ID',)
