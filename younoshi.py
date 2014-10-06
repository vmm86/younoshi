#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask

# Инициализация приложения
app = Flask(__name__, template_folder='view')

# login = app.route('/login', methods=['GET', 'POST'])(view.login)

import controller

if __name__ == '__main__':
    app.run()
