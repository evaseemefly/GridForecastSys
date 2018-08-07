# -*- coding:utf-8 -*-
__author__ = 'evaseemefly'
__date__ = '2018/3/10 12:46'

import json
from datetime import datetime,date,timedelta,time
from django.forms.models import model_to_dict

def query2json(query_set):
    json_list=[]
    for model in query_set:
        obj=model_to_dict(model)
        '''
        To use a custom JSONEncoder subclass
         (e.g. one that overrides the default() method to serialize additional types), 
         specify it with the cls kwarg; otherwise JSONEncoder is used.
        '''
        dic=json.dumps(obj,cls=CJsonEncoder)
        json_list.append(dic)
    return json_list


class CJsonEncoder(json.JSONEncoder):
    '''
    自定义的json序列化类，需要重写default方法
    '''
    def default(self, obj):
        '''
        解决date无法序列化的问题
        若传入的obj是一个date则str成 yyyy-mm-dd的
        :param obj:
        :return:
        '''
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
