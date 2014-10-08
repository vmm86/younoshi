#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask

# Инициализация приложения
app = Flask(__name__, template_folder = 'view')

from config import SessionConf, TestingConf

# Секретный ключ из файла конфигурации для создания пользовательской сессии
app.secret_key = SessionConf.SECRET_KEY

import controller

# Увязка функций из контроллера и URL-адресов, по которым они будут работать:

## Обработка ошибки 404
app.register_error_handler (404, controller.page_not_found)

## Главная страница
app.add_url_rule(
    '/',
    view_func = controller.index)
## Вход в систему
app.add_url_rule(
    '/login',
    view_func = controller.login, methods = ['GET', 'POST',])
## Выход из системы
app.add_url_rule(
    '/logout',
    view_func = controller.logout)

## Города
app.add_url_rule(
    '/city',
    view_func = controller.listCity)
### Добавление городов
app.add_url_rule(
    '/city/create',
    view_func = controller.createCity, methods = ['GET', 'POST',])
### Изменение городов
app.add_url_rule(
    '/city/<int:cityid>/update',
    view_func = controller.updateCity, methods = ['GET', 'POST',])
### Удаление городов
app.add_url_rule(
    '/city/<int:cityid>/delete',
    view_func = controller.deleteCity, methods = ['GET', 'POST',])

## Спортивные школы
app.add_url_rule(
    '/city/<int:cityid>/school',
    view_func = controller.listSchool)
### Добавление спортивных школ
app.add_url_rule(
    '/city/<int:cityid>/school/create',
    view_func = controller.createSchool, methods = ['GET', 'POST',])
### Изменение споривных школ
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/update',
    view_func = controller.updateSchool, methods = ['GET', 'POST',])
### Удаление спортивных школ
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/delete',
    view_func = controller.deleteSchool, methods = ['GET', 'POST',])

## Команды
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/team',
    view_func = controller.listTeam)
### Добавление команд
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/team/create',
    view_func = controller.createTeam, methods = ['GET', 'POST',])
### Изменение команд
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/update',
    view_func = controller.updateTeam, methods = ['GET', 'POST',])
### Удаление команд
app.add_url_rule(
    '/city/<int:cityid>/school/<int:schoolid>/team/<int:teamid>/delete',
    view_func = controller.deleteTeam, methods = ['GET', 'POST',])

## Стадии
app.add_url_rule(
    '/stage',
    view_func = controller.listStage)
### Добавление стадий
app.add_url_rule(
    '/stage/create',
    view_func = controller.createStage, methods = ['GET', 'POST',])
### Изменение стадий
app.add_url_rule(
    '/stage/<int:stageid>/update',
    view_func = controller.updateStage, methods = ['GET', 'POST',])
### Удаление стадий
app.add_url_rule(
    '/stage/<int:stageid>/delete',
    view_func = controller.deleteStage, methods = ['GET', 'POST',])

## Сезоны
app.add_url_rule(
    '/season',
    view_func = controller.listSeason)
### Добавление сезонов
app.add_url_rule(
    '/season/create',
    view_func = controller.createSeason, methods = ['GET', 'POST',])
### Изменение сезонов
app.add_url_rule(
    '/season/<int:seasonid>/update',
    view_func = controller.updateSeason, methods = ['GET', 'POST',])
### Удаление сезонов
app.add_url_rule(
    '/season/<int:seasonid>/delete',
    view_func = controller.deleteSeason, methods = ['GET', 'POST',])

## Игровые стадии
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage',
    view_func = controller.listSAS)
### Добавление игровых этапов
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/create',
    view_func = controller.createSAS, methods = ['GET', 'POST',])
### Изменение игровых этапов
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/update',
    view_func = controller.updateSAS, methods = ['GET', 'POST',])
### Удаление игровых этапов
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/delete',
    view_func = controller.deleteSAS, methods = ['GET', 'POST',])

## Команды в игровых этапах
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team',
    view_func = controller.listSAST)
### Добавление команд в игровые этапы
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/create',
    view_func = controller.createSAST, methods = ['GET', 'POST',])
### Изменение команд в игровых этапах
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/<int:sastid>/update',
    view_func = controller.updateSAST, methods = ['GET', 'POST',])
### Удаление команд в игровых этапах
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/team/<int:sastid>/delete',
    view_func = controller.deleteSAST, methods = ['GET', 'POST',])

## Игровые протоколы
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp',
    view_func = controller.listGP)
### Добавление игрового протокола
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/create',
    view_func = controller.createGP, methods = ['GET', 'POST',])
### Изменение игрового протокола
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/<int:gpid>/update',
    view_func = controller.updateGP, methods = ['GET', 'POST',])
### Удаление игрового протокола
app.add_url_rule(
    '/season/<int:seasonid>/age/<int:ageid>/stage/<int:sasid>/gp/<int:gpid>/delete',
    view_func = controller.deleteGP, methods  = ['GET', 'POST',])

app.debug = TestingConf.DEBUG

if __name__ == '__main__':
    app.run()
