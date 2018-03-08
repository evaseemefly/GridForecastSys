# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/3/6 16:24'

import numpy as np
import pandas as pd
import os
import sys
import datetime
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR,VARCHAR

class GridForecast:
    db_name='gridforecast_forecastdailyinfo'
    table_name='gridforecast'
    now_str='2018-03-07 00:00'

    def run(self):
        df=self.readcsv('convert_date.csv')
        df_value=self.getmaxvalue(df)
        df_date=self.getmaxdate(df)
        df_finall=self.df_concat(df_value,df_date,self.now_str)
        self.writeInDb(df_finall,self.db_name,self.table_name)

    def readcsv(self,path):
        # 1、读取转换好的结构化数据文件
        read_date=pd.read_csv(path,',')
        # 设置第一列和第二列为层次化索引
        read_date=read_date.set_index(['0','1'])
        read_date.index.names=['code','factor']
        return read_date

    def getmaxvalue(self,df):
        # 2-1、获取最大值的df
        df_max_value=df.T.max().unstack()
        # 为最大值的columns赋name
        df_max_value.columns=['DIR_VALUE','HS_VALUE','PER_VALUE']
        # 去掉index的name
        df_max_value.index=df_max_value.index.values
        return df_max_value

    def getmaxdate(self,df):

        # 2-2、获取最大值出现的时间
        df_max_date=df.T.idxmax(axis=0).unstack()
        df_max_date.columns=['DIR_DATE','HS_DATE','PER_DATE']
        # 去掉index的name
        df_max_date.index=df_max_date.index.values
        return df_max_date

    def df_concat(self,df_value,df_date,now_str):

        # 3、两个df拼接
        # axis=1 横向拼接
        final_data=pd.concat([df_date,df_value],axis=1)
        final_data['nowdate']=now_str
        # 批量更改列的数据类型
        final_data['DIR_DATE']=final_data['DIR_DATE'].astype('datetime64[ns]')
        final_data['HS_DATE']=final_data['HS_DATE'].astype('datetime64[ns]')
        final_data['PER_DATE']=final_data['PER_DATE'].astype('datetime64[ns]')
        final_data['nowdate']=final_data['nowdate'].astype('datetime64[ns]')
        # 由于当前的索引为网格的code，将索引设置为code列
        final_data['code']=final_data.index
        return final_data

    def writeInDb(self,df,db_name,table_name):

        # 4、连接数据库，并写入
        # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        # 注意若使用mysql+mysqlconnector 默认使用的是mysql-python（此模块已不再更新py3的版本）
        # connect=create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/gridforecast')
        engine = create_engine('mysql+mysqldb://admin:admin123@localhost:3306/gridforecast')
        dtypedict={
            'str':VARCHAR(length=4),
        }
        pd.io.sql.to_sql(df,db_name,engine,schema=table_name, if_exists='append',index=False,dtype=dtypedict)

grid= GridForecast()
grid.run()
