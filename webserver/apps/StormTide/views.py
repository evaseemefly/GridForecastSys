from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import APIView
import json

from .models import StormTideDailyInfo,StormTideInfo
from .serializers import StormTideDetailSerializer,StormTideSerializer

from Common import convertdate

'''
    1、根据指定时间获取该日的风暴潮、增水的极值及对应时间
'''

class StormTideDailyView(APIView):
    '''
        获取指定日期的风暴潮及增水的极值
    '''
    def get(self,request):
        '''
            获取请求中的时间（或有区域-area）
        :param request:
        :return:
        '''
        # 获取请求中的时间
        # 此处应加入判断，若不存在应返回错误信息
        target_date=request.GET.get('targetdate')
        target_date=convertdate.convertDate(target_date)
        list_stormtidedetail=StormTideDailyInfo.objects.filter(nowdate=target_date)
        json_data=StormTideDetailSerializer(list_stormtidedetail,many=True).data
        return Response(json_data)


class StormTideView(APIView):
    '''
        获取指定日期及指定海洋站的的72小时预报值
    '''
    def get(self,request):

        # 此处需要加入判断，若不存在，返回错误信息
        target_date=request.GET.get('targetdate')
        code=request.GET.get('code')
        list=StormTideInfo.objects.filter(date=target_date,code=code)
        json_data=StormTideSerializer(list,many=True).data
        return Response(json_data)


class MyTideView(APIView):
    def get(self,request):
        
        return Response()


