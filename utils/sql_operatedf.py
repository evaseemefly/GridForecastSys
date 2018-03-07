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
read_date.index.names=['code','factor']
final_data=read_date.T.idxmax(axis=0).unstack()

final_data['code']=read_date.T.idxmax(axis=0).unstack().index
final_data['nowdate']='2018-03-07 00:00'

# 去掉columns的names
final_data.columns=final_data.columns.values.tolist()

# 批量更改列的数据类型
final_data['DIR']=final_data['DIR'].astype('datetime64[ns]')
final_data['HS']=final_data['HS'].astype('datetime64[ns]')
final_data['PER']=final_data['PER'].astype('datetime64[ns]')
final_data['nowdate']=final_data['nowdate'].astype('datetime64[ns]')
# final_data=read_date.T.idxmax(axis=0).unstack()
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# 注意若使用mysql+mysqlconnector 默认使用的是mysql-python（此模块已不再更新py3的版本）
# connect=create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/gridforecast')
engine = create_engine('mysql+mysqldb://admin:admin123@localhost:3306/gridforecast')
insp=inspect
pd.io.sql.to_sql(final_data,'forecastdata',engine,schema='gridforecast', if_exists='replace',index=False)
if
pass

