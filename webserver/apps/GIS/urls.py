# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/10/24 10:47'

from django.conf.urls import url, include
from .views import WaveForceCastInfoView

app_name='[gis]'
urlpatterns = [
    #获取指定日期的预报数据
    url(r'^waveforcedetial/$', WaveForceCastInfoView.as_view(), name="gis-get-waveforcedetial")
]
