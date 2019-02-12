# bll业务逻辑层

from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings

'''
    模仿传统的三层中的业务逻辑层    
'''

class Connection:
    def __init__(self):
        '''
            1-实例化时初始化数据库引擎
            2-创建db session
        :param tablename:
        '''
        # 住一此处需要设置convert_unicode=true，默认为false
        self.engine=create_engine(settings.DB_CONNECT_STR,convert_unicode=True)
        Session=sessionmaker(bind=self.engine)
        self.session=Session()

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class BuoInfoBLL(Connection):
    def isExist(self,code):
        '''
            判断指定code是否已经 存在数据库中，不存在则创建
        :param code:
        :return:
        '''
        res = self.session.query(FubInfo). filter(FubInfo.code == code)
        res=res.all()
        if len(res)>0:
            return res[0]
        else:
            return None

    def create(self,fubinfo):
        '''
            写入
        :param fubinfo:
        :return:
        '''
        temp=FubInfo(name=fubinfo.name,
                      code=fubinfo.no,
                      remark='',
                      lat=fubinfo.lat,
                      lon=fubinfo.lon,
                     area='n',
                     isShow=True)

        self.session.add(temp)
        # 此处flush后，插入的temp中便有了自增的id
        self.session.flush()
        self.session.commit()
        return temp

class RealtimeInfoBLL(Connection):
    def create(self,realtime,fub,dt):
        '''
            添加至fub_realtime
        :param realtime:
        :return:
        '''
        temp=FubRealtimeInfo(ws=realtime.ws,
                             wd=realtime.wd,
                             bp=realtime.bp,
                             wv=realtime.ybg,
                             wvperiod=realtime.yzq,
                             wvd=realtime.wvd,
                             code=fub.code,
                             timestamp=dt,
                             fid_id=fub.id,
                             lat=fub.lat,
                             lon=fub.lon)

        self.session.add(temp)
        self.session.commit()