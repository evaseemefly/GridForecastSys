# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/8/6 15:32'

def convertDate(date_str):
    date="-".join([date_str[:4],date_str[4:6],date_str[6:8]])
    return date