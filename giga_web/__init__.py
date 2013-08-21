from flask import Flask
from make_celery import make_celery
from converter import ObjectIDConverter
from settings import ProductionConfig, DevelopmentConfig, TestingConfig
from celery.utils.log import get_task_logger

crud_url = 'https://crud.gigawatt.co'


giga_web = Flask('giga_web')
giga_web.config.from_object(DevelopmentConfig)
giga_web.url_map.converters['objectid'] = ObjectIDConverter
celery_logger = get_task_logger('giga_web')
celery = make_celery(giga_web)
#running celery requires this command:
#celery worker -A giga_web.celery --autoscale=4,2 -Q test_queue

from redis_lock import Lock, LockTimeout
import helpers
from giga_web import views, tasks, ext
