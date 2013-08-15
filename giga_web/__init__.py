from flask import Flask
from make_celery import make_celery
from converter import ObjectIDConverter
from settings import ProductionConfig, DevelopmentConfig, TestingConfig
from celery.utils.log import get_task_logger

crud_url = 'http://giga_crud_test.gigawatt.co'


giga_web = Flask(__name__)
giga_web.config.from_object(DevelopmentConfig)
giga_web.url_map.converters['objectid'] = ObjectIDConverter
celery_logger = get_task_logger(__name__)
celery = make_celery(giga_web)
#running celery requires this command:
#celery worker -A giga_web.celery --autoscale=4,2 -Q test_queue

from redis_lock import Lock, LockTimeout
import helpers
from giga_web import views, tasks, ext
