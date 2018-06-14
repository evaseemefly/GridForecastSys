import time,datetime,os
from celery_app import app
from core import DataFrameOperator
from conf import settings
# import datetime

@app.task
def add(x, y):
    time.sleep(2)
    return x + y

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y

@app.task
def convertData(sourcepath,filename,fileExt,midpath,midfile,midEXT):
    # 处理每日生成的文件转成.csv文件
    # tempdate=datetime.datetime(2018,5,20)
    # now_str = datetime.datetime.now().strftime('%Y%m%d')
    now_dt=datetime.datetime.now()

    # 获取每日预报特征数据
    grid_daily=DataFrameOperator.ForecastDailyInfo(now_dt)
    midfinialpath= grid_daily.run(sourcepath,filename,fileExt,midpath,midfile,midEXT)
    # 获取每日预报详细数据
    grid_detail=DataFrameOperator.ForecastDetailInfo(now_dt)
    grid_detail.run(midpath,midfile,midEXT)
