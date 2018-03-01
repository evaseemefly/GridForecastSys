# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/2/28 11:10'

import os
import numpy as np

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
        # 若传入的字典参数中指定了存取路径
        if kwargs['targetfile'] is not None:
            self.targetfile=kwargs['targetfile']
        np.load(self.targetfile)



