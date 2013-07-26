from flask import Flask
from make_celery import make_celery
from converter import ObjectIDConverter
from settings import ProductionConfig, DevelopmentConfig, TestingConfig

crud_url = 'http://giga_crud_test.gigawatt.co'


giga_web = Flask(__name__)
giga_web.config.from_object(DevelopmentConfig)
giga_web.url_map.converters['objectid'] = ObjectIDConverter
celery = make_celery(giga_web)

from giga_web import views, tasks
