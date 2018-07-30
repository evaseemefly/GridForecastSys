# -*- coding:utf-8 -*-
__author__='evaseemefly'

from django.db import models

# Create your models here.
class GridInfo(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,verbose_name=u"网格名称")
    code=models.CharField(max_length=5,verbose_name=u"网格编码")
    area=models.CharField(max_length=2,choices=(("n","北海"),("e","东海"),("s","南海")),verbose_name="所属区域")

    class Meta:
        verbose_name=u"网格信息"
        verbose_name_plural=verbose_name

class StationInfo(models.Model):
    '''
        海洋站详情
    '''
    id=models.AutoField(primary_key=True)
    # 父级节点
    pid=models.IntegerField(default=0)
    name=models.CharField(max_length=50,verbose_name=u"海洋站名称")
    code=models.CharField(max_length=6,verbose_name=u"海洋站站代码")
    area=models.CharField(max_length=2,choices=(("n","北海"),("e","东海"),("s","南海")),verbose_name="所属区域")

    class Meta:
        verbose_name=u"海洋站信息"
        verbose_name_plural=verbose_name
