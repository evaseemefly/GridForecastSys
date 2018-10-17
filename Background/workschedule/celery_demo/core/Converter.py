import abc
import os
import pandas as pd
import numpy as np

class BaseConverter(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self,readpath,readfilename):
        self.readpath=readpath
        self.readfilename=readfilename

    def inintData(self):
        '''
        读取csv文件，并设置index列
        :return:
        '''
        # 1、读取指定路径下的csv文件
        finialpath=os.path.join(self.readpath,self.readfilename)
        read_data=pd.read_csv(finialpath,',')

        # 2 获取所有的columns
        cols=list(read_data)

        # 1.2 获取'1'（factor）的所在位置，并移至第一列
        cols.insert(0, cols.pop(cols.index('1')))

        read_date = read_data.set_index(['1', '0'])

        df_convert_1 = read_date.T['HS']

        # 2、设置第一列第二列为联合索引
        # read_data=read_data.set_index(['0','1'])
        # 2-2设置联合索引的index的名字
        # read_data.index.names=['code','factor']
        def create_temp_df(df_convert_1, columns_key, nowday):
            df_new = pd.DataFrame(df_convert_1.loc[:, columns_key])
            #     print(df_new)
            df_new['code'] = columns_key
            df_new['date'] = nowday
            df_new = df_new.reset_index()
            df_new = df_new.rename(columns={'index': 'tdate'})
            df_new = df_new.rename(columns={columns_key: 'hs'})
            #     print(df_new)
            return df_new

        df_merage = pd.DataFrame(columns=['tdate', 'hs', 'code', 'date'])
        for val in df_convert_1.columns.values:
            df_temp = create_temp_df(df_convert_1, val, '2018-03-13')
            #     print(df_temp)
            df_merage = df_merage.append(df_temp)