# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/7/30 14:52'

from django.db import models
from django.db import models
from datetime import datetime

# from Station.models import StationInfo
# from Station.models import StationInfo
# Create your models here.

class StormTideInfo(models.Model):
    '''
        72小时的风暴潮及增水的实际预报值
    '''
    id = models.AutoField(primary_key=True)
    # CASCADE为默认的级联删除
    date=models.DateField(default=datetime.now)
    tdate=models.DateTimeField(default=datetime.now)
    # 增水
    surge=models.FloatField(default=-999.0)
    # 潮位
    tide=models.FloatField(default=-999.0)
    code=models.CharField(default='ERROR',max_length=6)

    class Meta:
        verbose_name=u"每日风暴潮及增水详细数据"
        verbose_name_plural=verbose_name

class StormTideDailyInfo(models.Model):
    '''
        每日的风暴潮及增水的极值（极大值）及出现时间
    '''
    id = models.AutoField(primary_key=True)
    # CASCADE为默认的级联删除
    Surge_DATE = models.DateTimeField(default=datetime.now)
    Tide_DATE = models.DateTimeField(default=datetime.now)
    nowdate = models.DateField(default=datetime.now)
    Surge_VALUE = models.FloatField(default=999.0)
    Tide_VALUE = models.FloatField(default=999.0)
    CODE = models.CharField(default='ERROR', max_length=6)
    class Meta:
        verbose_name=u"每日预报风暴潮及增水极值及时间"
        verbose_name_plural=verbose_name

class WaveRealtimeInfo(models.Model):
    '''
        wv报文
    '''
    wid=models.AutoField(primary_key=True)
    # 有效波高
    wv=models.FloatField(default=999.0)
    # 有效周期
    wvperiod=models.FloatField(default=999.0)
    # 波向
    wvd=models.IntegerField(default=999)
    code=models.CharField(max_length=6)
    sid=models.ForeignKey('Station.StationInfo',on_delete=models.CASCADE)
    # 时间戳
    timestamp=models.DateTimeField(default=datetime.now)

class WaveHistoryInfo(models.Model):
    '''
        wv报文（历史数据）
    '''
    wid=models.AutoField(primary_key=True)
    # 有效波高
    wv=models.FloatField(default=999.0)
    # 有效周期
    wvperiod=models.FloatField(default=999.0)
    # 波向
    wvd=models.IntegerField(default=999)
    code=models.CharField(max_length=6)
    sid=models.ForeignKey('Station.StationInfo',on_delete=models.CASCADE)
    # 时间戳
    timestamp=models.DateTimeField(default=datetime.now)
