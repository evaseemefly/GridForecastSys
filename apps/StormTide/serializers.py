# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/7/31 17:14'

from rest_framework import serializers
from .models import StormTideInfo,StormTideDailyInfo

class StormTideDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=StormTideDailyInfo
        fields=('__all__')