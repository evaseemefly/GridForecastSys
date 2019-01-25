from django.http import HttpRequest,HttpResponse,JsonResponse,Http404
from datetime import datetime,timedelta
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from pytz import timezone
from django.utils import timezone
from django.utils.timezone import utc
from django.http import HttpResponseRedirect
# 为视图使用的自定义装饰器
import pytz
# 自己的一些组件
# from common import DateCommon

tz_utc_8=pytz.timezone('Asia/Shanghai')
# tz_utc_8 = pytz.timezone(timedelta(hours=8))


def date_required(func):
    '''
        目标时间装饰器，若request中未含targetdate，则将当前日期付给requset
    :param func:
    :return:
    '''
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        try:
            start = request.GET.get('start', None)
            end=request.GET.get('end',None)
            kind= request.GET.get('kind','now')
            # utcnow=datetime.now()
            utcnow=timezone.now()
            # targetdate = targetdate if kind=='history' else datetime.now()
            start = start if kind == 'history' else utcnow
            if kind=='now' or end==None:
                end=start+timedelta(days=1)
                # now str转成 yyyy-mm-dd HH:mm
                # targetdate.strftime('%Y-%m-%d %H:%M')
                pass
            elif kind=='history':
                # history str时转成 yyyy-mm-dd
                # TODO
                start=datetime.strptime(start,'%Y-%m-%d').replace(tzinfo=utc)
                end=datetime.strptime(end,'%Y-%m-%d').replace(tzinfo=utc)
                # targetdate=targetdate+timedelta(hours=-8)
                # tzname = timezone.get_current_timezone_name()
                # targetdate=pytz.timezone(tzname).localize(targetdate)

            # 转换为世界时
            # targetdate=DateCommon.local2Utc(targetdate)
            # isNow=request.GET.get('isNow',True)
            request.GET=request.GET.copy()
            request.GET['start']=start
            request.GET['end']=end
            return func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404()
            # if redirect:
            #     return HttpResponseRedirect(redirect)
            # else:
            #     raise Http404()

    return returned_wrapper

def data_loaclUtc(func):
    '''
        将本地时间转换为世界时
    :param func:
    :return:
    '''
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        try:
            targetdate = request.GET.get('targetdate', None)
            # 转为世界时
            utcDate=DateCommon.local2Utc(targetdate)
            request.GET = request.GET.copy()
            request.GET['targetdate'] = utcDate
            return func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404()
            # if redirect:
            #     return HttpResponseRedirect(redirect)
            # else:
            #     raise Http404()

    return returned_wrapper

def history_requeired(func):
    '''
        实时历史数据装饰器
        请求中若未包含kind，则默认赋值给now（获取当前）
    :param func:
    :return:
    '''
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        try:
            kind=request.GET.get('kind','now')
            request.GET=request.GET.copy()
            request.GET['kind']=kind
            return func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404()
            # if redirect:
            #     return HttpResponseRedirect(redirect)
            # else:
            #     raise Http404()

    return returned_wrapper