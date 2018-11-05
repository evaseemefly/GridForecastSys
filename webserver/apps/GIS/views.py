from django.shortcuts import render

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
import json

import datetime
import numpy as np
from Common.ncReader import NCEnvironment
from Common.MyMath import getRundingVal

from .model_middle import WaveModel
from .serializers import WaveModelSerializer
# Create your views here.
class WaveForceCastInfoView(APIView):
    '''
        加载每日的240小时海浪预报值
    '''
    def get(self,request):
        params_dic=request.query_params
        lat=float(params_dic.get('lat'))
        lat=getRundingVal(lat,0.25)
        lng=float(params_dic.get('lng'))
        lng=getRundingVal(lng,0.25)
        targetDate=params_dic.get('date')
        read= NCEnvironment('nc_reader')
        # 获取最终的数组
        finall_arr= read.read(lat,lng)
        # 判断数组的长度
        # 获取日期数组
        # 根据传入的起始时间，通过时间间隔6小时为间隔，生成时间数组
        index=0
        beginDate=datetime.datetime.strptime(targetDate,'%Y%m%d%H')
        dates=[]
        temp_date=beginDate
        dates.append(temp_date)
        while index<40:
            index=index+1
            temp_date=temp_date+datetime.timedelta(hours=6)
            dates.append(temp_date)

        wave_list = [WaveModel(temp[0],temp[1]) for temp in zip(dates,finall_arr)]
        json_list=WaveModelSerializer(wave_list,many=True).data
        # wave_list=[WaveModel(dates[index],temp) for temp,index in finall_arr]
        # finall_array= np.dstack((np.array(dates),np.array(finall_arr)))
        return Response(json_list)
        # return JsonResponse(finall_arr)
        # pass

