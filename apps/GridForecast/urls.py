# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/3/10 10:47'

from django.conf.urls import url, include
from .views import ForecastDailyInfoView,ForecastHomeView

app_name='[forecast]'
urlpatterns = [
    #获取指定日期的预报数据
    url(r'^daily/(?P<date>[0-9]{8})/(?P<area>\S*)/$', ForecastDailyInfoView.as_view(), name="forecast-get-dailyforecast"),

    url(r'^home/$',ForecastHomeView.as_view() , name="forecast-home"),
]