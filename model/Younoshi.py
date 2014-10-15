#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import Model

from connect import younoshi_db

# Определение модели - базового класса модели, который определяет, какую БД использовать.
# Все его подкласссы будут наследовать указанное в нём хранинище.
class Younoshi(Model):
    class Meta:
        database = younoshi_db
