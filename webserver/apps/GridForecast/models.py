# -*- coding:utf-8 -*-
__author__='evaseemefly'


from django.db import models
from datetime import datetime
# from .models import GridInfo
from Station.models import GridInfo
# Create your models here.

# Create your models here.
# class GridInfo(models.Model):
#     id=models.AutoField(primary_key=True)
#     name=models.CharField(max_length=50,verbose_name=u"网格名称")
#     code=models.CharField(max_length=5,verbose_name=u"网格编码")
#     area=models.CharField(max_length=2,choices=(("n","北海"),("e","东海"),("s","南海")),verbose_name="所属区域")
#
#     class Meta:
#         verbose_name=u"网格信息"
#         verbose_name_plural=verbose_name

class ForecastDetailInfo(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateField(default=datetime.now)
    tdate=models.DateTimeField(default=datetime.now)
    hs = models.FloatField(default=-999.0)
    code = models.CharField(default='ERROR', max_length=6)

    class Meta:
        verbose_name=u"每日预报详细数据"
        verbose_name_plural=verbose_name

class ForecastInfo(models.Model):
    id=models.AutoField(primary_key=True)
    # CASCADE为默认的级联删除
    gid=models.ForeignKey(GridInfo,verbose_name=u"网格信息",on_delete=models.CASCADE,)
    generatedate=models.DateField(default=datetime.now)
    max_value=models.FloatField()
    max_date=models.DateField(default=datetime.now)
    max_per=models.FloatField()
    min_value=models.FloatField()
    min_date=models.DateField(default=datetime.now)
    min_per=models.FloatField()

    class Meta:
        verbose_name=u"预报数据"
        verbose_name_plural=verbose_name

class ForecastDailyInfo(models.Model):
    id = models.AutoField(primary_key=True)
    # CASCADE为默认的级联删除
    DIR_DATE=models.DateTimeField(default=datetime.now)
    HS_DATE=models.DateTimeField(default=datetime.now)
    PER_DATE=models.DateTimeField(default=datetime.now)
    nowdate=models.DateField(default=datetime.now)
    DIR_VALUE=models.FloatField(default=999.0)
    HS_VALUE=models.FloatField(default=999.0)
    PER_VALUE=models.FloatField(default=999.0)

    CODE=models.CharField(default='ERROR',max_length=6)
    # gid = models.CharField(max_length=4,default=None)
    # generatedate = models.DateField(default=datetime.now)
    # max_value = models.FloatField()
    # max_date = models.DateField(default=datetime.now)
    # max_per = models.FloatField()
    # min_value = models.FloatField()
    # min_date = models.DateField(default=datetime.now)
    # min_per = models.FloatField()
    class Meta:
        verbose_name=u"每日预报数据极值及条件"
        verbose_name_plural=verbose_name
