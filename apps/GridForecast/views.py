# -*- coding:utf-8 -*-
__author__='evaseemefly'


from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import APIView
import json



from .models import ForecastDailyInfo,ForecastDetailInfo
from .serializers import ForecastDetailInfoSerializer
from utils import queryset2json


# Create your views here.
def convertDate(date_str):
    date="-".join([date_str[:4],date_str[4:6],date_str[6:8]])
    return date

class ForecastDetialInfoView(APIView):
    '''
    获取指定日期以及code的72小时预报值
    '''
    def get(self,request,date,code):
        data=self.getTargetCodeDetialData(date,code)
        # return JsonResponse({'error': 'Some error'}, status=401)
        return Response(data)

    def getTargetCodeDetialData(self,date,code):
        '''
        获取指定日期以及code的72小时预报值
        :param date:
        :param code:
        :return:
        '''
        # 根据code以及预报生成的日期获取对应的预报值（72小时）
        date_converted= convertDate(date)
        # detialinfo=ForecastDetailInfo.objects.all()[:5]
        detialinfo= ForecastDetailInfo.objects.filter(Q(code=code)&Q(date=date_converted))
        detialinfo_serializer=ForecastDetailInfoSerializer(detialinfo,many=True)
        return detialinfo_serializer.data


class ForecastHomeView(View):
    def get(self,request):
        return render(request, "home-new.html")

class ForecastDailyInfoView(View):
    '''
    查询指定日期及区域的72小时极大值以及对应的时间
    '''
    def get(self,request,date,area='a'):
        '''
        根据指定的日期以及区域获取该日的数据
        :param request:
        :param date:
        :param area:
        :return:
        '''
        forecastinfo_date_all_qs= self.getDateMaxForecastInfo(date,area)
        # json_data=serializers.serialize("json",forecastinfo_date_all_qs,ensure_ascii=False)
        '''
            序列化的方式1：
                使用django自带的serializers.serialize
                * 先使用此种方式
        '''
        json_data = serializers.serialize("json", forecastinfo_date_all_qs, ensure_ascii=False,fields=('id','HS_DATE','HS_VALUE','CODE'))

        '''
            序列化的方式2：
                使用自定义的将query转成json的方法
        '''
        json_list=queryset2json.query2json(forecastinfo_date_all_qs)
        # 错误如下：AttributeError: 'str' object has no attribute '_meta'
        # json_data_dict=model_to_dict(json_list)
        json_data_dump=json.dumps(json_list,default=lambda obj:obj.__dict__,ensure_ascii=False)
        return HttpResponse(json_data_dump,content_type='application/json')


    def getDateMaxForecastInfo(self,date,area):
        '''
        根据指定日期获取该日的所有极值预报
        :param date:
        :return:
        '''
        # 获取当日的全部的极值预报
        # 注意此处传过来的date是 20180302这种形式的，需要转换
        # 使用''.join的方式可以以指定的形式拼接后面的参数（类型：list）
        # date_convert="-".join([date[:4],date[4:6],date[6:8]])
        date_convert=convertDate(date)
        # 由于在数据库中保存的area都是大写的，此处需要处理一下
        area=area.upper()
        if area!='A':
            # forecastinfo_date_all = ForecastDailyInfo.objects.filter(Q(CODE__contains=area))
            forecastinfo_date_all= ForecastDailyInfo.objects.filter(Q(nowdate=date_convert)&Q(CODE__contains=area))
        else:
            forecastinfo_date_all=ForecastDailyInfo.objects.filter(nowdate=date_convert)
        return forecastinfo_date_all
