# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/11/17 10：05'

from rest_framework.response import Response
from rest_framework.decorators import APIView

import datetime
import time

#为特定请求方法添加装饰器
from django.utils.decorators import method_decorator

# model
from .models import FubDataInfo,FubInfo
from Common.decorator_view import *

# 序列化对象
from .serializers import FubInfoSerializer,FubDataInfoSerializer,FubRealtimeInfoSerializer,FubRealtimeInfoMidSerializer,RealtimeWdWsSerializer,RealtimeSimpSerializer
# base views
from .views_base import RealtimeBaseView,FubBaseView
# Create your views here.

from apps.MyCelery.tasks import add

class GridView(APIView):
    def get(self,request,code):
        pass

# 获取全部浮标的列表
class FubAllView(FubBaseView):
    '''
        获取全部浮标的列表
    '''
    def get(self,request):
        list=self.getAllFub()
        json_data = FubInfoSerializer(list, many=True)
        return Response(json_data.data)
        # list_fub=FubInfo.objects.filter(isShow=True)
        # json_data=FubInfoSerializer(list_fub,many=True)
        # return Response(json_data.data)

class FubFilterListView(APIView):
    '''
        根据传入的 ids 以及 nowdate 获取指定的fub的信息
    '''
    def get(self,request):
        # params_dic = request.query_params
        # request.GET.getlist('ids')
        # 获取fub的id
        # list_id=params_dic.get('ids')
        # 获取指定fub的ids
        list_ids=request.GET.getlist('ids[]')
        target_date_str=request.GET.get('nowdate')
        # 将传入的nowdate转换为date类型
        target_date=datetime.datetime.strptime(target_date_str,'%Y-%m-%d')

        # 2 根据ids进行查询
        # 下面处理关于datetime对象的筛查问题：
        # 方式1：
        # 使用__year,__month,__day的方式进行筛选 不可行
        # list_fub_data=FubDataInfo.objects.filter(fid__in=list_ids,tdate__year=target_date.year,tdate__month=target_date.month,tdate__day=target_date.day)
        # list_fub_data = FubDataInfo.objects.filter(fid__in=list_ids, tdate=target_date)
        # list_fub_data = FubDataInfo.objects.filter(tdate__year=target_date.year,
        #                                           tdate__month=target_date.month,
        #                                           tdate__day=target_date.day)
        # 时间查询加入两个条件会出错
        # list_fub_data = FubDataInfo.objects.filter(tdate__year=2018,tdate__month=11)
        # list_fub_data = FubDataInfo.objects.filter(tdate__year='2018',tdate__month='11')
        # 方式2：
        # 链式筛查 不行
        # list_fub_data = FubDataInfo.objects.filter(tdate__year=2018).filter(tdate__month=11).filter(tdate__day=19)

        # 方式3
        # 单个筛选 可行
        # list_fub_data = FubDataInfo.objects.filter(tdate__year=2018)

        # 方式4
        # 对当前的日期加上23：59：59 可行
        # now = datetime.datetime.now()
        target_date_finish= target_date+datetime.timedelta(hours=23, minutes=59, seconds=59)
        # list_fub_data = FubDataInfo.objects.filter(tdate__date__gte=now)
        list_fub_data=FubDataInfo.objects.filter(tdate__gt=target_date,tdate__lt=target_date_finish,fid__id__in=list_ids)
        # list_fub_data = FubDataInfo.objects.filter(tdate__date__gt=datetime.date(2018,11, 17))
        # json_data=FubDataInfoSerializer(list_fub_data,many=True)
        json_data=FubDataInfoSerializer(list_fub_data,many=True)
        return Response(json_data.data)
        # pass


class FubDailyDataView(APIView):
    '''
        获取指定浮标，指定时间的72小时预报值
    '''
    def get(self,request):
        # 获取指定fub的ids
        id = request.GET.get('fid')
        target_date_str = request.GET.get('nowdate')
        # 将传入的nowdate转换为date类型
        target_date_later = datetime.strptime(target_date_str, '%Y-%m-%d %H:%M')

        # 2 根据ids进行查询
        # 下面处理关于datetime对象的筛查问题：
        # 方式4
        # 对当前的日期加上23：59：59 可行
        target_date_early = target_date_later - timedelta(days=1)
        # list_fub_data=FubRealtimeInfo.objects.filter(timestamp__gte=target_date_early,timestamp__lte=target_date_later,fid_id=id)
        # list_fub_data = FubDataInfo.objects.filter(tdate__gt=target_date_early, tdate__lt=target_date_later,fid__id=id)
        # json_data = FubDataInfoSerializer(list_fub_data, many=True)
        # json_data=FubRealtimeInfoSerializer(list_fub_data,many=True)
        pass
        # return Response(json_data.data)

# 获取fub最后传输的时间的观测值
class FubLastRealtimeView(RealtimeBaseView,APIView):
    '''
        获取fub最后传输的时间的观测值
    '''
    def get(self,request):
        area=request.GET.get('area','a')

        list=self.getAllFubLastRealtimeList(area)
        json_data=FubRealtimeInfoMidSerializer(list,many=True).data
        return Response(json_data)

# 根据时间进行过滤获取指定fid的指定时间内的观测数据
class FubFilterDataView(RealtimeBaseView,APIView):
    '''
        根据时间进行过滤获取指定fid的指定时间内的观测数据
    '''
    @method_decorator(date_required)
    def get(self,request):
        fid=int(request.GET.get('fid',-1))
        start=request.GET.get('start')
        end=request.GET.get('end')
        list=self.getDateRangFubData(fid,start,end)
        json_data=FubRealtimeInfoSerializer(list,many=True).data
        return Response(json_data)

class FubInfoView(APIView):
    '''
        获取浮标基础数据
    '''
    def get(self,request):
        fid=int(request.GET.get('fid',-1))
        # 需要大写
        code=request.GET.get('code','').upper()

        list=FubInfo.objects.filter(code=code)
        json_data=FubInfoSerializer(list,many=True).data
        return Response(json_data)


class RealtimeListView(RealtimeBaseView):
    def get(self,request):
        factor = request.GET.get('factor', '')
        fid = int(request.GET.get('fid', -1))
        code=request.GET.get('code','')
        dateRangeStr = request.GET.get('dateRange', '')
        kind = request.GET.get('kind')
        # 此处加一个判断，若未传入target，则将当前的时间赋给targetdate
        targetdate = request.GET.get('targetdate', None)
        targetdate = targetdate if targetdate is not None else datetime.now().strftime('%Y-%m-%d')
        try:
            tmp_arr = dateRangeStr.split(' ')
            start_date=tmp_arr[0]
            end_date=tmp_arr[1]
            start_date = datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M')
            end_date = datetime.strptime(end_date + ' 23:59', '%Y-%m-%d %H:%M')
        except Exception  as e:
            now =  datetime.strptime(targetdate,'%Y-%m-%d')

            (start_date,end_date)=(now - timedelta(hours=24),now) if kind=='now' else (now,now+timedelta(hours=24))

        list= self.getTargetFactorList(start_date,end_date,factor,fid,code=code)
        json_data= RealtimeWdWsSerializer(list,many=True).data if (factor=='wd' or factor=='ws') else RealtimeSimpSerializer(list,many=True).data
        # json_data=RealtimeSimpSerializer(list,many=True).data
        return Response(json_data)


class FubTaskView(APIView):
    '''
        引入celery的测试视图
    '''
    def get(self,request):
        result=add.delay(2,10)
        return Response(None)