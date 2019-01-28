# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/11/17 10：05'

from django.db import models

from datetime import datetime
# Create your models here.

class FubInfo(models.Model):
    '''
        浮标信息
        注意去掉经纬度（因为浮标的经纬度有时会变动，不宜放在一张固定的表中）
    '''
    id=models.AutoField(primary_key=True)
    code=models.CharField(max_length=10,verbose_name=u"浮标站位号")
    name=models.CharField(max_length=20,null=True,verbose_name=u"浮标名称")
    remark=models.CharField(max_length=200,verbose_name=u"备注",null=True)
    # 是否显示
    isShow=models.BooleanField(default=True)
    Lon = models.FloatField(max_length=6, null=True,verbose_name="经度")
    Lat = models.FloatField(max_length=6,null=True, verbose_name="维度")
    area_choices=(
        ('QD','beihai'),
        ('SH','donghai'),
        ('GZ','nanhai'),
        ('OT','other')
    )
    area=models.CharField(
        max_length=2,
        choices=area_choices,
        default='OT'
    )
    class Meta:
        verbose_name=u"浮标信息"
        verbose_name_plural=verbose_name

class FubDataInfo(models.Model):
    '''
        浮标详细数据
    '''
    id=models.AutoField(primary_key=True)
    fid=models.ForeignKey('FubInfo',on_delete=models.CASCADE)
    # 指定时间
    tdate=models.DateTimeField(default=datetime.now)
    # 最大波高
    wv=models.FloatField(null=True)
    # 波向
    wvc=models.IntegerField(null=True)
    # 周期
    period=models.FloatField(null=True)

    class Meta:
        verbose_name=u"浮标观测数据"
        verbose_name_plural=verbose_name

class FubRealtimeInfo(models.Model):
    '''
        浮标的观测数据（实时）只保留一周
    '''
    wid=models.AutoField(primary_key=True)
    # 风速
    ws=models.FloatField(default=999.9)
    # 风向
    wd=models.FloatField(default=999.9)
    # 气压
    bp=models.FloatField(default=9999.9)
    # 有效波高
    wv=models.FloatField(default=999.9)
    # 有效周期
    wvperiod=models.FloatField(default=999.9)
    # 波向
    wvd=models.IntegerField(default=999)
    code=models.CharField(max_length=6)
    fid=models.ForeignKey('FubInfo',on_delete=models.CASCADE)
    # 时间戳
    timestamp=models.DateTimeField(default=datetime.now)
    lon=models.FloatField(max_length=6,verbose_name="经度")
    lat=models.FloatField(max_length=6,verbose_name="纬度")