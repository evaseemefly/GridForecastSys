# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/3/21 9:44'

from rest_framework import serializers
from .models import  ForecastDetailInfo

class ForecastDetailInfoSerializer(serializers.ModelSerializer):
    # 注意此处不要继承错了，不要继承：serializers.Serializer
     class Meta:
         model=ForecastDetailInfo
         fields = ('tdate', 'hs')
