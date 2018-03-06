# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/3/6 16:24'

import numpy as np
import pandas as pd
import os
import sys
import datetime
from sqlalchemy import create_engine


read_date=pd.read_csv('convert_date.csv',',')
# read_date=read_date.set_index([0,1])
read_date.head()
read_date=read_date.set_index(['0','1'])
final_data=read_date.T.idxmax(axis=0).unstack()
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
connect=create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/gridforecast')
pass

