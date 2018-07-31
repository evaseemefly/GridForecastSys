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
from .serializers import StormTideDetailSerializer

'''
    1、根据指定时间获取该日的风暴潮、增水的极值及对应时间
'''

class StormTideDailyView(APIView):
    def get(self,request):
        '''
            获取请求中的时间（或有区域-area）
        :param request:
        :return:
        '''
        # 获取请求中的时间
        target_date=request.GET.get('targetdate')
        list_stormtidedetail=StormTideDailyInfo.objects.filter(nowdate=target_date)
        json_data=StormTideDetailSerializer(list_stormtidedetail,many=True).data
        return Response(json_data)


