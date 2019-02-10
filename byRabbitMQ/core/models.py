
from lxml import etree
import os
from datetime import datetime
import re

# sqlalchemy
from sqlalchemy import Column, String, create_engine,Integer,Float,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Create your models here.

Base=declarative_base()

class BuoyInfo(Base):
    __tablename__=''
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
        self.dt=dt

    id=Column(Integer,primary_key=True)
    type=Column(String(5))
    name=Column(String(10))
    no=Column(String(10))
    Kind=Column(String(10))
    lat=Column(Float)
    lon=Column(Float)
    dt=Column(DateTime)


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

    fid_id = Column(Integer, primary_key=True)
    ws = Column(Float)
    wd = Column(Float)
    at = Column(Float)
    bp = Column(Float)
    hu = Column(Float)
    wt = Column(Float)
    sl = Column(Float)
    bg = Column(Float)
    wv = Column(Float)
    wvd = Column(Float)

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
            isExists=os.path.exists(self.dir)
            if isExists:
                os.chdir(self.dir)
                return True
            else:
                return False
        except Exception as exc:
            print(exc)
            return False


    def _readFile(self):
        # 先判断指定路径是否存在，并切换
        if self._switchDir():
            # 以xml的方式读取指定文件
            self.fileData=etree.parse(self.filename)

    def getRoot(self):
        root = self.fileData.getroot()
        if len(list(root)) == 1:
            return (root if root.tag == 'OceanObservatingDataFile' else None)

    def latlonConvert(self,str):
        temp=re.match(r'\d+[°][0-9]+[.]([0-9]{2})',str).group(0).split('°')
        temp=int(temp[0])+float(temp[1])/60
        temp=float(format(temp,'.2f'))
        return temp

    @property
    def fubInfo(self):
        '''
            读取xml文件中的BuoyageRpt节点下的BuoyInfo与lat，long与datetime
        :return:
        '''
        if(self.fileData==None):
            self._readFile()
        try:
            root=self.getRoot()
            # buoyageRpt=self.fileData.getchildren()[0]
            buoyageRpt = root.getchildren()[0]
            buoyInfo=buoyageRpt.find('BuoyInfo')
            # 1 获取buoyInfo
            # 2 获取lat与lon
            location = buoyageRpt.find('BuoyInfo').getchildren()[0]
            lon = self.latlonConvert(location.get('longitude',''))
            lat = self.latlonConvert(location.get('latitude',''))
            # 3 获取时间
            dt = buoyageRpt.find('DateTime').get('DT')
            dt=datetime.strptime(dt,'%Y%m%d%H%M')

            buoyInfo=BuoyInfo(buoyInfo.get('Type'),buoyInfo.get('id'),buoyInfo.get('Name'),buoyInfo.get('NO'),buoyInfo.get('Kind'),lat,lon,dt)
            return buoyInfo
        except AttributeError as ex:
            print(ex)

    @property
    def realtimeInfo(self):
        '''
            读取xml文件中的HugeBuoyData节点->BuoyData : Realtime数据
        :return:
        '''
        if (self.fileData == None):
            self._readFile()
        root = self.getRoot()
        buoyageRpt = root.getchildren()[0]
        realData=buoyageRpt.find('HugeBuoyData').find('BuoyData')
        realtimeInfo=RealtimeInfo(float(realData.get('WS')),float(realData.get('WD')),float(realData.get('AT')),float(realData.get('BP')),float(realData.get('HU')),float(realData.get('WT')),float(realData.get('SL')),float(realData.get('BG')),float(realData.get('YBG')),float(realData.get('YZQ')))
        return realtimeInfo
