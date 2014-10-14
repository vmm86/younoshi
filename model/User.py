#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import PrimaryKeyField, CharField

from connect import *

## Пользователи
class User(Younoshi):
    user_ID = PrimaryKeyField(
        db_column = 'user_ID')
    userLogin = CharField(
        db_column  = 'userLogin',
        max_length = 32,
        null       = False)
    userPassword = CharField(
        db_column  = 'userPassword',
        max_length = 32,
        null       = False)
    userName = CharField(
        db_column  = 'userName',
        max_length = 32,
        null       = False)

    class Meta:
        db_table = 'User'
        order_by = ('user_ID',)
