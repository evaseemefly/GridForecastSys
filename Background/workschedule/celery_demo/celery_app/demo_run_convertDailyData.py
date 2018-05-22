# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/5/21 12:30'

from conf import settings
from celery_app import tasks

task=tasks.convertData(settings.TARGET_READ_TODAY_PATH,settings.GRID_DAILY_SOURCE_FILENAME,settings.GRID_DAILY_SOURCE_EXT,settings.TARGET_SAVE_MID_PATH,settings.GRID_DAILY_MID_FILENAME,settings.GRID_DAILY_MID_EXT)