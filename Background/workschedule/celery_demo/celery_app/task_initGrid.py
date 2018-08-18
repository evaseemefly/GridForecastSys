import time

import sys,os
from conf.settings import TARGET_DJANGO_PROJ_PATH
sys.path.append(TARGET_DJANGO_PROJ_PATH)

from celery_app import app

from django.core.wsgi import get_wsgi_application
from django.core.management import setup_environ

import GridForecastSys.settings
from apps.Station.models import GridInfo
import utils.file_readgrids

os.environ.setdefault("DJANGO_SETTINGS_MODULE","GridForecastSys.settings")
application = get_wsgi_application()
setup_environ(GridForecastSys.settings)
# from GridForecastSys import settings

def init():
    print(GridForecastSys.settings.AreaNames_Dict)

init()

def initGrid():
    for key in GridForecastSys.settings.AreaNames_Dict:
        value = GridForecastSys.settings.AreaNames_Dict[key] + ".txt"
        save_gridinfo(key, GridForecastSys.settings.AreaNames_DIR, value)

def save_gridinfo(self,area_key,dir,filename):
    '''
    保存网格数据至数据库
    :param dir:
    :param filename:
    :return:
    '''

    # 1 读取指定路径下的文件
    areainfo=utils.file_readgrids.AreaNamesFileInfo(dir,filename)
    # 1.1 获取该文件中的网格名称(dataframe)
    area_df= areainfo.readNamesFile()
    grid_list=list()
    for index,row in area_df.iterrows():
        code=area_key.upper()+str(index+1).zfill(2)
        grid_list.append(GridInfo(name=row[0],code=code,area=area_key))
    # 2 批量更新数据库
    GridInfo.objects.bulk_create(grid_list)
