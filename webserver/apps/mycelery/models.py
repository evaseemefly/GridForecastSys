from django.db import models

from lxml import etree
import os
from datetime import datetime
# Create your models here.

class BuoyInfo:
    '''
        浮标基础信息
    '''
    def __init__(self,type,id,name,no,Kind,lat,lon,dt):
        self.type=type
        self.id=id
        self.name=name
        self.no=no
        self.kind=Kind
        self.lat=lat
        self.lon=lon

class RealtimeInfo:
    '''
        浮标数据中的观测值
    '''
    def __init__(self,ws,wd,at,bp,hu,wt,sl,bg,ybg,yzq):
        self.ws=ws
        self.wd=wd
        self.at=at
        self.bp=bp
        self.hu=hu
        self.wt=wt
        self.sl=sl
        self.bg=bg
        self.ybg=ybg
        self.yzq=yzq

class OceanObservationgData:
    '''
        浮标海洋观测数据
    '''
    fileData=None
    def __init__(self,dir,filename):
        '''
            浮标海洋观测数据
        :param filename:
        '''
        self.filename=filename
        self.dir=dir

    def _switchDir(self):
        '''
            切换当前堵路路径
        :return:
        '''
        # 先判断指定路径是否存在
        try:
            os.path.exists(self.dir)
            os.chdir(self.dir)
            return True
        except Exception as exc:
            print(exc)
            return False


    def _readFile(self):
        # 先判断指定路径是否存在，并切换
        if self._switchDir():
            # 以xml的方式读取指定文件
            self.fileData=etree.parse(self.filename)

    @property
    def fubInfo(self):
        '''
            读取xml文件中的BuoyageRpt节点下的BuoyInfo与lat，long与datetime
        :return:
        '''
        if(self.fileData==None):
            self._readFile()
        buoyageRpt=self.fileData.getchildren()[0]
        # 1 获取buoyInfo
        # 2 获取lat与lon
        location = buoyageRpt.find('BuoyInfo').getchildren()[0]
        lon = location.get('longitude')
        lat = location.get('latitude')
        # 3 获取时间
        dt = buoyageRpt.find('DateTime').get('DT')
        dt=datetime.strptime(dt,'%Y%m%d%H%M')

        buoyInfo=BuoyInfo(buoyageRpt.get('Type'),buoyageRpt.get('id'),buoyageRpt.get('Name'),buoyageRpt.get('NO'),buoyageRpt.get('Kind'),lat,lon,dt)
        return buoyInfo

    @property
    def realtimeInfo(self):
        '''
            读取xml文件中的HugeBuoyData节点->BuoyData : Realtime数据
        :return:
        '''
        if (self.fileData == None):
            self._readFile()
        buoyageRpt = self.fileData.getchildren()[0]
        realData=buoyageRpt.find('HugeBuoyData').find('BuoyData')
        realtimeInfo=RealtimeInfo(realData.get('WS'),realData.get('WD'),realData.get('AT'),realData.get('BP'),realData.get('HU'),realData.get('WT'),realData.get('SL'),realData.get('BG'),realData.get('YBG'),realData.get('YZQ'))
        return realtimeInfo


