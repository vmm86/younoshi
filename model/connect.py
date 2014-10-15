#! /usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

from peewee import MySQLDatabase

from config import DatabaseConf

dbname   = DatabaseConf.DB_NAME
dbpasswd = DatabaseConf.DB_PASSWD
dbuser   = DatabaseConf.DB_USER

# Создание экземпляра базы данных Peewee.
# Все модели будут использовать его для сохранения информции.
younoshi_db = MySQLDatabase(dbname, passwd = dbpasswd, user = dbuser)

# Создание и удаление подключения к БД по каждому запросу.

# from flask import g

# @app.before_request
# def before_request():
#     g.db = younoshi_db
#     g.db.connect()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response
