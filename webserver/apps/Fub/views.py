# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/11/17 10：05'

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import APIView

import datetime

# model
from .models import FubDataInfo,FubInfo

# 序列化对象
from .serializers import FubInfoSerializer,FubDataInfoSerializer
# Create your views here.

class GridView(APIView):
    def get(self,request,code):
        pass

class FubAllView(APIView):
    '''
        获取全部浮标的列表
    '''
    def get(self,request):
        list_fub=FubInfo.objects.filter(isShow=True)
        json_data=FubInfoSerializer(list_fub,many=True)
        return Response(json_data.data)

class FubFilterListView(APIView):
    '''
        根据传入的id获取指定的fub
    '''
    def get(self,request):
        # params_dic = request.query_params
        # request.GET.getlist('ids')
        # 获取fub的id
        # list_id=params_dic.get('ids')
        # 获取指定fub的ids
        list_ids=request.GET.getlist('ids')
        target_date_str=request.GET.get('nowdate')
        # 将传入的nowdate转换为date类型
        target_date=datetime.datetime.strptime(target_date_str,'%Y-%m-%d')
        # 2 根据ids进行查询
        # list_fub_data=FubDataInfo.objects.filter(fid__in=list_ids,tdate__year=target_date.year,tdate__month=target_date.month,tdate__day=target_date.day)
        # list_fub_data = FubDataInfo.objects.filter(fid__in=list_ids, tdate=target_date)
        list_fub_data = FubDataInfo.objects.filter(tdate__year=target_date.year,
                                                  tdate__month=target_date.month, tdate__day=target_date.day)
        json_data=FubDataInfoSerializer(list_fub_data,many=True)
        return Response(json_data.data)
        # pass



