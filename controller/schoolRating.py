#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from model import schoolRating

from User import login_required

## Рейтинг команд
@login_required
def schoolRating():
    listSR = schoolRating.select()

    return render_template(
        'schoolRating.jinja.html', 
        listSR = listSR)
