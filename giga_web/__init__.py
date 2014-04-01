from flask import Flask
from giga_web.ext.ses_mailer import SES_Mailer
from flask.ext.mongoengine import MongoEngine
from make_celery import make_celery
from settings import ProductionConfig, TestConfig
from celery.utils.log import get_task_logger


giga_web = Flask('giga_web')
giga_web.config.from_object(TestConfig)
celery_logger = get_task_logger('giga_web')
celery = make_celery(giga_web)
mailer = SES_Mailer(giga_web)
db = MongoEngine(giga_web)
db.init_app(giga_web)
#running celery requires this command:
#celery worker -A giga_web.celery --autoscale=4,2 -Q test_queue

import helpers
from giga_web import views, tasks, ext, models
