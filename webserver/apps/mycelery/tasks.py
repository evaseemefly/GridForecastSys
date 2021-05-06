from __future__ import absolute_import
from celery import shared_task

#
from .models import OceanObservationgData
# from settings import READ_DIR
from .settings import READ_DIR

Read_Dir=READ_DIR

@shared_task
def add(x,y):
    return x+y


def readFubXml(filename):
    oceanData=OceanObservationgData(Read_Dir,filename)
    fubInfo=oceanData.fubInfo
    realtimeInfo=oceanData.realtimeInfo


# TODO:[-] 21-05-06 暂时去掉此部分
# readFubXml('201312051000qf101.dat.xml.xml')