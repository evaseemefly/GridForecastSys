import os,sys
from celery.schedules import crontab


BROKER_URL = 'redis://127.0.0.1:6379'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend
CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'
CELERY_IMPORTS = (                                  # 指定导入的任务模块
    # 'celery_app.task1',
    # 'celery_app.task2',
    'celery_app.tasks'
)

# 指定的django项目的项目根目录
# TARGET_DJANGO_PROJ_PATH=r'D:\git仓库\GridForecastSys'
# TARGET_READ_TODAY_PATH=r'D:\git仓库\GridForecastSys\demo_data'
# TARGET_SAVE_PATH=r'D:\git仓库\GridForecastSys\result'
# TARGET_SAVE_MID_PATH=r'D:\git仓库\GridForecastSys\result'

# 单位的配置
TARGET_DJANGO_PROJ_PATH=r'D:\git仓库\GridForecastSys'
TARGET_READ_TODAY_PATH=r'D:\git仓库\GridForecastSys\demo_data'
TARGET_SAVE_PATH=r'D:\git仓库\GridForecastSys\result'
TARGET_SAVE_MID_PATH=r'D:\git仓库\GridForecastSys\result'

# 提供的每日数值预报产品的名字
GRID_DAILY_SOURCE_FILENAME='BasicUnit_'
GRID_DAILY_SOURCE_EXT='.txt'

# 生成的每日预报文件中间生成的文件名（前缀）
GRID_DAILY_MID_FILENAME='convert_data'
GRID_DAILY_MID_EXT='.csv'

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERYBEAT_SCHEDULE = {

    'add': {

        'task': 'celery_app.tasks.convertData',

        'schedule': crontab(hour=9,minute=5),

        'args': (TARGET_READ_TODAY_PATH,
                 GRID_DAILY_SOURCE_FILENAME,GRID_DAILY_SOURCE_EXT,
                 TARGET_SAVE_MID_PATH,GRID_DAILY_MID_FILENAME,GRID_DAILY_MID_EXT)

    }
}
