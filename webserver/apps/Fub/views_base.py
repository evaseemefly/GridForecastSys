

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
from .middle_model import RealtimeMidInfo
# 序列化对象
from .serializers import FubInfoSerializer,FubDataInfoSerializer

# TODO 定义的前后端factor不同的对照字典
dict_factor={
    'ws':'ws',          # 风速
    'wd':'wd',          # 风向
    'bp':'bp',          # 气压
    'ybg':'wv',         # 有效波高
    'yzq':'wvperiod',   # 有效波周期
}

class RealtimeBaseView(APIView):
    '''
        浮标实时数据的基类
    '''
    def _getTargetFubRealtimeInfo(self,code,start,end=None):
        '''
            根据起止时间获取指定时间内的指定fub数据
        :param start:
        :param end:
        :return:
        '''
        if end is None:
            list=FubRealtimeInfo.objects.filter(timestamp=start,code=code)
        else:
            list=FubRealtimeInfo.objects.filter(timestamp__gte=start,timestamp__lte=end,code=code)
        return list

    def getTargetFactorList(self,start,end,factor,fid=-1,**kwargs):
        '''
            获取指定船舶的指定要素观测值
        :param fid:
        :param start:
        :param end:
        :param factor:
        :return:
        '''

        # 对于风速与风向，要同时获取
        code=''
        # TODO 注意此处需要转换一下（还需要加入判断）
        factor=dict_factor.get(factor)
        if fid==-1 and kwargs.get('code')!=None:
            code=kwargs.get('code')
        if factor=='ws' or factor=='wd':
            list=self._getTargetFubRealtimeInfo(code,start,end).order_by('timestamp').values('timestamp','wd','ws')
            # list=list[:3]
            list_convert = [RealtimeMidInfo(temp['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                                {'ws':temp['ws'].__round__(2),
                                 'wd':temp['wd']})
                            for temp in list]
        else:

            list = self._getTargetFubRealtimeInfo(code,start,end).order_by('timestamp').values('timestamp',factor)
            list_convert=[RealtimeMidInfo(temp['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),temp[factor].__round__(2)) for temp in list]
        #为了如果没得到任何结果，让屏幕显示点东西
        if len(list_convert) == 0:
            # 对于风向风速为val填充{}，其他默认填充0
            defaultAppend= lambda :{} if (factor=='wd' or factor=='ws') else 0
            dict_first = {'timestamp':start.strftime('%Y-%m-%d %H:%M:%S'),'val':defaultAppend()}
            dict_last={'timestamp':end.strftime('%Y-%m-%d %H:%M:%S'),'val':defaultAppend()}
            list_convert.append(dict_first)
            list_convert.append(dict_last)
        return list_convert

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
        # list_finall = list.values('ws', 'wd', 'bp', 'bp', 'wv', 'wvperiod', 'wvd', 'code', 'fid', 'lon', 'lat',
        #                           'timestamp').filter(timestamp__in=list_max.values_list('max_time')).annotate(max_time=Max('timestamp')).annotate(count_fid=Count('fid'))
        # list_finall = list.values('ws', 'wd', 'bp', 'bp', 'wv', 'wvperiod', 'wvd', 'code', 'fid', 'lon', 'lat',
        #                           'timestamp').select_related()
        # list_finall=[]
        list_finall=[(list.filter(fid__id=obj['fid'], timestamp=obj['max_time'])[0]) for obj in list_max]
        # (list_finall.append(list.filter(fid__id=obj['fid'], timestamp=obj['max_time'])[0]) for obj in list_max)
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

