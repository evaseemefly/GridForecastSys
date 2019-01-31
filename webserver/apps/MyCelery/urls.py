from django.conf.urls import url, include
from .views import *
urlpatterns=[
#获取指定日期的预报数据
    # url(r'^station/(?P<code>\S*)/$', FubAllView.as_view(), name="station-get-station"),
    # 获取全部浮标的列表
    url(r'^test/$',Test.as_view(),name="fub-all"),
]