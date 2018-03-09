# -*- coding:utf-8 -*-
__author__='evaseemefly'

import numpy as np
import pandas as pd

import os
import sys

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse
from django.core import serializers

import json

from utils.file_readgrids import AreaNamesFileInfo
from GridForecastSys import settings
# import GridForecastSys.settings

from Station.models import GridInfo

def getgrid(request,num=1):
    num1=num
    pass

class Grid(View):
    def post(self,request):
        self.initGrid()

    def get(self,request, forecastdate=None, area=None):
    # def get(self,request,num=1):
        '''

        :param forecastdate:
        :param area:
        :return:
        '''
        # date=num
        self.getarea(area)
        pass

    def getarea(self,area):
        '''
        根据传入的area获取指定区域的信息list
        :param area:
        :return:
        '''
        data=None
        if area!='all':
            # targetAreas=GridInfo.objects.get(area)
            targetAreas=GridInfo.objects.filter(area=area)
            list_areas=list(targetAreas)
            data=serializers.serialize("json",targetAreas,ensure_ascii=False)
            # 用此种方法会报错：TypeError: Object of type 'GridInfo' is not JSON serializable
            databyjson=json.dumps(list_areas)
        # data=
        print(area)
        print(databyjson)
        return HttpResponse(data,content_type='application/json')

    def initGrid(self):
        '''
        初始化网格
        '''
        # area_info=AreaNamesFileInfo()
        # 遍历字典：
        # for kv in settings.AreaNames_Dict:
        for key in settings.AreaNames_Dict:
            value=settings.AreaNames_Dict[key]+".txt"
            self.save_gridinfo(key,settings.AreaNames_DIR,value)

    def save_gridinfo(self,area_key,dir,filename):
        '''
        保存网格数据至数据库
        :param dir:
        :param filename:
        :return:
        '''

        # 1 读取指定路径下的文件
        areainfo=AreaNamesFileInfo(dir,filename)
        # 1.1 获取该文件中的网格名称(dataframe)
        area_df= areainfo.readNamesFile()
        grid_list=list()
        for index,row in area_df.iterrows():
            code=area_key.upper()+str(index+1).zfill(2)
            grid_list.append(GridInfo(name=row[0],code=code,area=area_key))
        # 2 批量更新数据库
        GridInfo.objects.bulk_create(grid_list)
        pass



