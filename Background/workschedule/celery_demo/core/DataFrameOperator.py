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
import abc

class DataFrameInfo(metaclass=abc.ABCMeta):
    # __metaclass__==abc.ABCMeta
    df_base=None
    def __init__(self,dt=datetime.datetime.now()):
        self.now_dt=dt
        self.now_str=dt.strftime('%Y%m%d')
        self.mid_finialPath=None

    def writeInDb(self,df,db_name,table_name):
        # 4、连接数据库，并写入
        # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        # 注意若使用mysql+mysqlconnector 默认使用的是mysql-python（此模块已不再更新py3的版本）
        # connect=create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/gridforecast')
        # 单位台式机配置
        engine = create_engine('mysql+mysqldb://admin:admin123@localhost:3306/gridforecast')
        # aw配置
        # engine = create_engine('mysql+mysqldb://root:admin123@localhost:3306/gridforecast')
        dtypedict={
            'str':VARCHAR(length=4),
        }
        pd.io.sql.to_sql(df,table_name,engine,schema=db_name, if_exists='append',index=False,dtype=dtypedict)

    def toCSV(self,midPath,filename,fileEXT):
        finialpath=os.path.join(midPath,filename+self.now_str+fileEXT)
        self.df_base.to_csv(finialpath)
        return finialpath

    def readcsv(self,sourcepath,filename,fileEXT):
        '''
        读取原文件
        :param path:
        :return:
        '''
        # 1、读取转换好的结构化数据文件
        midfilefullpath=os.path.join(sourcepath,filename+self.now_str+fileEXT)
        print(midfilefullpath)
        with open(midfilefullpath,encoding='utf-8') as f:
            '''
                以下详细数据及尝试详见:
                02-读取72小时预报文件-finial-精简版
            '''
            data = pd.read_table(f, sep='\t', encoding='utf-8', header=None, infer_datetime_format=True)
            # 读取第一行
            columns_date = data.iloc[0]
            # 删除所有包含空值的列
            columns_date_notnan = columns_date[columns_date.notnull()]
            columns_date_notnan_convert = columns_date_notnan
            source_data=data
            # 读取除去第一行的其余数据
            data = data[1:]
            # 更改索引
            data = data.set_index([0, 1])
            # 修改head
            data.columns = columns_date_notnan_convert
            # read_date=pd.read_csv(f,',',encoding = "gbk")
            # 设置第一列和第二列为层次化索引
            # read_date=data.set_index(['0','1'])
            data.index.names=['code','factor']
        self.df_base=data
        return data


    @abc.abstractclassmethod
    def run(self,sourcepath,filename,fileEXT):
        '''
        需要由子类继承得执行方法
        :param path:
        :return:
        '''
        return


class ForecastDailyInfo(DataFrameInfo):
    '''
        每日预报的特征数据
    '''
    db_name='gridforecast'
    table_name='gridforecast_forecastdailyinfo'
    # now_str='2018-03-14 00:00'

    def __init__(self,dt):
        super(ForecastDailyInfo, self).__init__(dt)
        # self.now_str=dt.strftime('%Y-%m-%d')

    def run(self,sourcepath,filename,fileEXT,midpath,midfilename,midEXT):
        '''

        :param sourcepath:
        :param filename:
        :param fileEXT:
        :param midpath:
        :param midfilename:
        :param midEXT:
        :return:
        '''

        def merageToCSV(df):
            targetfilename = "convert_date.csv"
            final_path = os.path.join(targetfilename)
            df.to_csv(final_path)
        def readCSV():
            read_data = pd.read_csv('convert_date.csv')
            return read_data

        # 读取csv源文件
        df=self.readcsv(sourcepath,filename,fileEXT)
        merageToCSV(df)
        df_temp= readCSV()
        print('%s-%s-%s'%(sourcepath,filename,fileEXT))
        # print(df_temp)
        df_temp=df_temp.set_index(['code','factor'])
        # 获取最大值，df格式返回
        df_value=self.__getmaxvalue(df_temp)
        # 获取最大值所在的日期，df格式返回
        df_date=self.__getmaxdate(df_temp)
        # 将以上两个df拼接
        df_finall=self.__df_concat(df_value,df_date,self.now_str)
        # 写入数据库
        self.writeInDb(df_finall,self.db_name,self.table_name)
        finialpath=self.toCSV(midpath,midfilename,midEXT)
        return finialpath



    def __getmaxvalue(self,df):

        # 2-1、获取最大值的df
        df_max_value=df.T.max().unstack()
        # 为最大值的columns赋name
        df_max_value.columns=['DIR_VALUE','HS_VALUE','PER_VALUE']
        # 去掉index的name
        df_max_value.index=df_max_value.index.values
        return df_max_value



    def __getmaxdate(self,df):

        # 2-2、获取最大值出现的时间
        df_max_date=df.T.idxmax(axis=0).unstack()
        df_max_date.columns=['DIR_DATE','HS_DATE','PER_DATE']
        # 去掉index的name
        df_max_date.index=df_max_date.index.values
        return df_max_date

    def __df_concat(self,df_value,df_date,now_str):

        # 3、两个df拼接
        # axis=1 横向拼接
        final_data=pd.concat([df_date,df_value],axis=1)
        final_data['nowdate']=self.now_dt
        # 批量更改列的数据类型
        final_data['DIR_DATE']=final_data['DIR_DATE'].astype('datetime64[ns]')
        final_data['HS_DATE']=final_data['HS_DATE'].astype('datetime64[ns]')
        final_data['PER_DATE']=final_data['PER_DATE'].astype('datetime64[ns]')
        final_data['nowdate']=final_data['nowdate'].astype('datetime64[ns]')
        # 由于当前的索引为网格的code，将索引设置为code列
        final_data['code']=final_data.index
        return final_data

    # def writeInDb(self,df,db_name,table_name):
    #
    #     # 4、连接数据库，并写入
    #     # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    #     # 注意若使用mysql+mysqlconnector 默认使用的是mysql-python（此模块已不再更新py3的版本）
    #     # connect=create_engine('mysql+mysqlconnector://admin:admin123@localhost:3306/gridforecast')
    #     engine = create_engine('mysql+mysqldb://admin:admin123@localhost:3306/gridforecast')
    #     dtypedict={
    #         'str':VARCHAR(length=4),
    #     }
    #     pd.io.sql.to_sql(df,table_name,engine,schema=db_name, if_exists='append',index=False,dtype=dtypedict)

class ForecastDetailInfo(DataFrameInfo):
    '''
    每日预报详细数据
    '''
    db_name = 'gridforecast'
    table_name = 'gridforecast_forecastdetailinfo'
    # now_str = '2018-03-14 00:00'

    def __init__(self,dt):
        super(ForecastDetailInfo, self).__init__(dt)

    def run(self,sourcepath,filename,fileEXT):
        with open(os.path.join(sourcepath,filename+self.now_str+fileEXT), encoding='utf-8') as f:
            read_date=pd.read_csv(f, sep=',', encoding='utf-8', infer_datetime_format=True)


        # if self.df_base!=None:
        #     read_date=self.df_base
        # 1 转换df
        df_convert=self.__convert_df(read_date)
        # 2生成要写入数据库的df
        df_merage = pd.DataFrame(columns=['tdate', 'hs', 'code', 'date'])
        for val in df_convert.columns.values:
            df_temp = self.__create_temp_df(df_convert, val, self.now_str)
            #     print(df_temp)
            df_merage = df_merage.append(df_temp)
        self.writeInDb(df_merage, self.db_name, self.table_name)


    def __convert_df(self,df):
        '''
        处理原始dataframe，生成转换后的df（index为预报时间，columns为网格名称）
        :param df:
        :return:
        '''
        #1.1 获取所有的columns
        cols = list(df)
        #1.2 获取'1'（factor）的所在位置，并移至第一列
        # cols.insert(0, cols.pop(cols.index('1')))
        cols.insert(0, cols.pop(cols.index('factor')))
        # 2 设置0与1列为层次索引
        # read_date = df.set_index(['0', '1'])
        read_date = df.set_index(['factor', 'code'])
        # 3 生成转换后的df（index为预报时间，columns为网格名称）
        df_convert = read_date.T['HS']
        return df_convert

    def __create_temp_df(self,df_convert_1, columns_key, nowday):
        '''
        以列名作为新的df的code，提取hs数据
        :param columns_key:
        :param nowday:
        :return:
        '''
        df_new = pd.DataFrame(df_convert_1.loc[:, columns_key])
        #     print(df_new)
        df_new['code'] = columns_key
        df_new['date'] = nowday
        df_new = df_new.reset_index()
        df_new = df_new.rename(columns={'index': 'tdate'})
        df_new = df_new.rename(columns={columns_key: 'hs'})
        #     print(df_new)
        return df_new

# grid= ForecastDailyInfo()
# grid= ForecastDetailInfo()
# grid.run('convert_date.csv')

