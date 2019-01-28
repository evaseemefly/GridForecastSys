

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import APIView
from django.db.models import Max,Count

import datetime

# model
from .models import FubDataInfo,FubInfo,FubRealtimeInfo

# 序列化对象
from .serializers import FubInfoSerializer,FubDataInfoSerializer

class RealtimeBaseView(APIView):
    '''
        浮标实时数据的基类
    '''
    def getTargetFubRealtimeInfo(self,fid,start,end=None):
        '''
            根据起止时间获取指定时间内的指定fub数据
        :param start:
        :param end:
        :return:
        '''
        if end is None:
            list=FubRealtimeInfo.objects.filter(timestamp=start,fid__id=fid)
        else:
            list=FubRealtimeInfo.objects.filter(timestamp__gte=start,timestamp__lte=end,fid__id=fid)
        return list

    def getAllFubLastRealtimeList(self,area):
        '''
            获取所有浮标的最后时刻的数据
        :return:
        '''
        if area=='a':
            list=FubRealtimeInfo.objects
        else:
            list=FubRealtimeInfo.objects.filter(fid__area=area)
        # 对fid进行去重
        # list=list.values('ws','wd','bp','bp','wv','wvperiod','wvd','code','fid','lon','lat').annotate(Max('timestamp'),fid_count=Count('fid__id'))
        # list.group_by('fid').annotate(Max('timestamp'))
        # list = list.values('ws', 'wd', 'bp', 'bp', 'wv', 'wvperiod', 'wvd', 'code', 'fid', 'lon', 'lat').annotate(
        #     Max('timestamp'),fid_count=Count('fid__id'))
        # list = list.values('ws','wd','bp','bp','wv','wvperiod','wvd','code','fid','lon','lat').annotate(Max('timestamp'))

        '''
            -- 使用子查询连接的方式（可行）
            SELECT *
            FROM
            Fub_fubrealtimeinfo as f
            JOIN(SELECT
            fid_id, MAX(`timestamp`)
            MAX_TIME
            FROM
            Fub_fubrealtimeinfo as fr
            GROUP
            BY
            fid_id) as temp
            ON
            temp.fid_id = f.fid_id and temp.MAX_TIME = f.
            `timestamp`
        '''

        # list_temp=list.group_by('fid').annotate(Max('timestamp')).values('fid',max_time=)
        list_max = list.values('fid').annotate(max_time=Max('timestamp'))
        # list_finall=list.values('ws','wd','bp','bp','wv','wvperiod','wvd','code','fid','lon','lat','timestamp').filter(fid__in=list_max.values_list('fid'),timestamp__in=list_max.values_list('max_time'))
        list_finall = list.values('ws', 'wd', 'bp', 'bp', 'wv', 'wvperiod', 'wvd', 'code', 'fid', 'lon', 'lat',
                                  'timestamp').filter(timestamp__in=list_max.values_list('max_time')).annotate(max_time=Max('timestamp')).annotate(count_fid=Count('fid'))
        return list_finall

    def getDateRangFubData(self,fid,start,end):
        '''
            获取指定id的之间段内的数据
        :param fid:
        :param start:
        :param end:
        :return:
        '''
        # list = FubRealtimeInfo.objects.filter(fid__id=fid,)
        list=FubRealtimeInfo.objects.filter(fid__id=fid,timestamp__lte=end,timestamp__gte=start)
        return list

class FubBaseView(APIView):
    '''
        浮标操作基础类
    '''
    def getAllFub(self):
        '''
            获取全部的fub集合
        :return:
        '''
        list_fub = FubInfo.objects.filter(isShow=True)

