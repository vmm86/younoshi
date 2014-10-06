#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/vmm/www/younoshi')

from younoshi import app as application

reload(sys)
sys.setdefaultencoding('utf-8')
