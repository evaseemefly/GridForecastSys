from datetime import timedelta
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
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERYBEAT_SCHEDULE = {

    'add': {

        'task': 'celery_app.tasks.add',

       'schedule': crontab(hour=21,minute=8),

       'args': (16, 1)

    }
}