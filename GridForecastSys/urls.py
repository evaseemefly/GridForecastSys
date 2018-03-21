"""GridForecastSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.views.generic import TemplateView

from Station.views import Grid


urlpatterns = [
    path('admin/', admin.site.urls),
    url('^gridinit/$',Grid.as_view(),name='init'),
    url('^getgrid/(?P<forecastdate>[0-9]{8})/(?P<area>\S*)/$',Grid.as_view(),name='getgrid'),
    # 获取预报数据，并指定命名空间
    url('^forecast/',include('GridForecast.urls', namespace='forecast')),

    # url(r'^getgrid/(?P<forecastdate>[0-9]+)/$',Grid.as_view(),name='getgrid'),

    # django resut framework
    url(r'^api-auth/',include('rest_framework.urls'))
]
