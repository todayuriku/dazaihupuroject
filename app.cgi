#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

activate_this = "/home/users/2/muu-e566b10689/web/chitabea.com/poetech/dazaihuproject/venv/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

# Flaskアプリのパスを設定
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == "__main__":
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
