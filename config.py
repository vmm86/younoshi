#! /usr/bin/python
# -*- coding: utf-8 -*-

# Базовая конфигурация

class DatabaseConf(object):
    NAME   = 'younoshi'
    USER   = 'root'
    PASSWD = 'ckpvmm86'

class SessionConf(object):
    SECRET_KEY = '~a8a<uccng{,3}fr$[#n5\*s=h7"2n=}jhd-?y6dbb8a(n6+esykqy'

class TestingConf(object):
    DEBUG = True
    # TRAP_BAD_REQUEST_ERRORS = True
