# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/5/21 12:30'

import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from conf import settings
from celery_app import tasks

tasks.convertData(settings.TARGET_READ_TODAY_PATH,
                  settings.GRID_DAILY_SOURCE_FILENAME,settings.GRID_DAILY_SOURCE_EXT,
                  settings.TARGET_SAVE_MID_PATH,settings.GRID_DAILY_MID_FILENAME,settings.GRID_DAILY_MID_EXT)