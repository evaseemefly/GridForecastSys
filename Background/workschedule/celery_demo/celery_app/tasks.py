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

def convertData(sourcepath,filename,fileExt,midpath,midfile,midEXT):
    # 处理每日生成的文件转成.csv文件
    tempdate=datetime.datetime(2018,5,20)
    grid_daily=DataFrameOperator.ForecastDailyInfo(tempdate)

    now_str=datetime.datetime.now().strftime('%Y%m%d')
    midfinialpath= grid_daily.run(sourcepath,filename,fileExt,midpath,midfile,midEXT)

    grid_detail=DataFrameOperator.ForecastDetailInfo(tempdate)
    grid_detail.run(midpath,midfile,midEXT)
