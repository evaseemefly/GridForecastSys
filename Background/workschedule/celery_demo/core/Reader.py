import abc
import numpy as np
import pandas as pd
import os,sys
import datetime

class BaseReader(object):
    '''
    读取类的抽象父类
    '''
    __metaclass__=abc.ABCMeta

    def __init__(self,readpath, readfilename,convertpath,convertfilename='convert_date.csv'):
        self.readpath=readpath
        self.readfilename=readfilename
        self.convertpath=convertpath
        self.convertfilename=convertfilename

    @abc.abstractclassmethod
    def loadfile(self):
        '''
        抽象方法，需要子类实现，读取文件的方法
        :return:
        '''
        return

    @abc.abstractclassmethod
    def savefile(self,data,targetpath=None,targetfile=None):
        return

class dailyGridDataReader(BaseReader):
    fullName=None
    '''
    读取每日生成的网格化预报产品

    '''
    def loadfile(self):
        '''
        读取每日生成的网格化预报产品的文件，并返回data
        :return:
        '''
        #1 读取预报文件
        with open(self.fullName, "rb") as f:
            #     columns_date=pd.read_table(f,sep='\t',encoding='utf-8',nrows=1,header=None)
            data = pd.read_table(f, sep='\t', encoding='utf-8', header=None, infer_datetime_format=True)
            print('读取成功')
        return data

    def convert_data(self,data):
        '''
        对传入的data进行转换，并返回data
        :param data:
        :return:
        '''
        #2 读取第一行
        columns_date = data.iloc[0]

        # 转成list
        columns_date_notnan = columns_date[columns_date.notnull()]
        columns_date_notnan_convert = columns_date_notnan

        #3 读取出去第一行的其余数据
        data = data[1:]

        #4 更改索引
        data = data.set_index([0, 1])

        #5 修改head
        data.columns = columns_date_notnan_convert

        # 转置
        # 暂时先不转置
        # data.T
        return data



    def savefile(self,data,targetpath=None,targetfile=None):
        '''
        将转换好的data存储直指定路径下
        :param data:
        :param targetpath:
        :param targetfile:
        :return:
        '''
        # 若未传入新的生成路径以及文件名，则使用构造函数中的
        if targetpath is not None:
            self.convertpath = targetpath
        if targetfile is not None:
            self.convertfilename = targetfile
        #6 存储成csv文件
        # targetfilename = "convert_date.csv"
        final_path = os.path.join(self.convertpath, self.convertfilename)
        if data!=None:
            data.to_csv(final_path)
            print(final_path)


