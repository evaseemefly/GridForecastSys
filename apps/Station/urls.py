# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/6/14 21:01'

from django.conf.urls import url, include
from .views import GridView,StationView

app_name='[station]'
urlpatterns = [
    #获取指定日期的预报数据
    url(r'^station/(?P<code>\S*)/$', StationView.as_view(), name="station-get-station"),

]