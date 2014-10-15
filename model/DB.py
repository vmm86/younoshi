#! /usr/bin/python
# -*- coding: utf-8 -*-

from peewee import Model, Proxy

proxy_db = Proxy()

# Определение модели - базового класса модели, который определяет, какую БД использовать.
# Все его подклассы будут наследовать указанное в нём хранинище.
class DB(Model):
    class Meta:
        database = proxy_db
