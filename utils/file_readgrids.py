# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/2/28 11:10'
import numpy as np
import pandas as pd

import os
import sys
'''
读取txt文件
'''

class FileInfo():
    def __init__(self,dirpath,filename):
        '''

        :param dirpath:
        :param filename:
        '''
        self.dirpath=dirpath;
        self.filename=filename;
        self.targetfile=os.path.join(self.dirpath,self.filename)

    def readFile(self,**kwargs):
        '''
        读取指定路径下的文件，并返回其中的数据集
        :param kwargs:
        :return:
        '''
        # 若传入的字典参数中指定了存取路径
        # if kwargs.has_key('targetfile'):
        if kwargs.__contains__('targetfile'):
        # if kwargs['targetfile'] is not None:
            self.targetfile=kwargs['targetfile']
        # np.load(self.targetfile)
        with open(self.targetfile, "rb") as f:
            df = pd.read_table(f, encoding='utf-8', header=None)
        return df

class AreaNamesFileInfo(FileInfo):
    def __init__(self,dirpath,filename):
        super(AreaNamesFileInfo, self).__init__(dirpath,filename)

    def readNamesFile(self,**kwargs):
        '''
        读取指定路径下的区域名称文件
        :param kwargs:
        :return:
        '''
        df= self.readFile(**kwargs)
        return df

    def push2List(self,**kwargs):
        # 读取文件
        df= self.readNamesFile(**kwargs)
        grid_arr=[]
        for temp in df:

            grid_arr.append()





