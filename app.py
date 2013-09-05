#!/usr/bin/env python
#*-*coding:utf-8*-*
#
from __future__ import with_statement

import sys
import json
import logging
import logging.config

from flask import Flask


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config.from_object('config')

logging.config.fileConfig("logging.conf")
LOG = logging.getLogger(__name__)

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
