# -*- coding: utf-8 -*-
from celery import Celery
import conf
app = Celery('demo',include=['celery_app.tasks'])                                # 创建 Celery 实例
app.config_from_object('conf.settings')