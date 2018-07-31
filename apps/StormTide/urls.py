# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/7/30 14:52'

from django.conf.urls import url,include
from .views import StormTideDailyView

app_name='[storm]'
urlpatterns = [
    #获取指定日期的预报数据
    url(r'^daily$', StormTideDailyView.as_view(), name="storm-get-stormtidedetail"),

]