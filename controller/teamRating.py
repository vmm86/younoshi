#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import teamRating

from User import login_required

## Рейтинг команд
@login_required
def listTR():
    listTR = teamRating.select()

    return render_template(
        'teamRating.jinja.html', 
        listTR = listTR)
