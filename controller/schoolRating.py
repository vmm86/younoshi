#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from werkzeug.exceptions import default_exceptions, BadRequest, HTTPException, NotFound

from peewee import DoesNotExist

from model import Season, Age, schoolRating

from User import login_required

## Рейтинг команд
@login_required
def listSR(seasonid_from, seasonid_to):
    listSeason = Season.select().order_by(Season.seasonName)
    # listAge    = Age.select().order_by(Age.ageName)

    try:
        seasonname_from = Season.get(season_ID = seasonid_from).seasonName
        seasonname_to   = Season.get(season_ID = seasonid_to).seasonName
        # agename         = Age.get(age_ID = ageid).ageName
    except DoesNotExist:
        seasonname_from = None
        seasonname_to   = None
        # agename         = None

    listSR = schoolRating.select().where(schoolRating.season_ID.between(seasonid_from, seasonid_to))
    listSR_count = listSR.count()

    return render_template(
        'schoolRating.jinja.html', 
        listSeason    = listSeason, 
        seasonid_from = seasonid_from, 
        seasonid_to   = seasonid_to, 
        # listAge       = listAge, 
        # ageid         = ageid, 
        listSR        = listSR,
        listSR_count  = listSR_count)
