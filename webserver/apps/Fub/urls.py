# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/11/17 10：05'

from django.conf.urls import url, include
from .views import FubAllView,FubFilterListView
app_name='[Fub]'

urlpatterns=[
#获取指定日期的预报数据
    # url(r'^station/(?P<code>\S*)/$', FubAllView.as_view(), name="station-get-station"),
    # 获取全部浮标的列表
    url(r'^list/$',FubAllView.as_view(),name="fub-all"),
    url(r'^filterlist/$',FubFilterListView.as_view(),name="fub-filter")
]