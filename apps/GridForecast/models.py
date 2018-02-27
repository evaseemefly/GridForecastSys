# -*- coding:utf-8 -*-
__author__='evaseemefly'


from django.db import models
from datetime import datetime
# from .models import GridInfo
# from apps.Station.models import GridInfo
# Create your models here.

# Create your models here.
class GridInfo(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,verbose_name=u"网格名称")
    code=models.CharField(max_length=5,verbose_name=u"网格编码")
    area=models.CharField(max_length=2,choices=(("n","北海"),("e","东海"),("s","南海")),verbose_name="所属区域")

    class Meta:
        verbose_name=u"网格信息"
        verbose_name_plural=verbose_name

class ForecastInfo(models.Model):
    id=models.AutoField(primary_key=True)
    gid=models.ForeignKey(GridInfo,verbose_name=u"网格信息")
    generatedate=models.DateField(default=datetime.now)
    max_value=models.FloatField(decimal_places=1)
    max_date=models.DateField(default=datetime.now)
    max_per=models.FloatField(decimal_places=1)
    min_value=models.FloatField(decimal_places=1)
    min_date=models.DateField(default=datetime.now)
    min_per=models.FloatField(decimal_places=1)

    class Meta:
        verbose_name=u"预报数据"
        verbose_name_plural=verbose_name

