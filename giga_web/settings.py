from kombu import Queue, Exchange
import urllib


class Config(object):
    DEBUG = False
    TESTING = False
    CELERY_BROKER_URL = 'sqs://%s:%s@' % (urllib.quote('AKIAJXUZNWCYS2DR7FNQ', safe=''),
                                          urllib.quote('cS7aurMhMikyk9/8y43UPQSnne5Zva+JuF1xPqgL', safe=''))
    CELERY_IMPORTS = ('giga_web.tasks')
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'America/New_York'


class ProductionConfig(Config):
    DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS = 'ec2-54-226-128-157.compute-1.amazonaws.com'
    REDIS_PORT = 6379
    REDIS_DB = 1
    CELERY_DEFAULT_QUEUE = 'test'
    CELERY_QUEUES = (
        Queue('test-donation_confirms', Exchange('test-donation_confirms'), routing_key='test.#'),
        Queue('test-update_project', Exchange('test-update_project'), routing_key='test.#'),
        Queue('test-update_campaign', Exchange('test-update_campaign'), routing_key='test.#'),
        Queue('test-update_leaderboard', Exchange('test-update_leaderboard'), routing_key='test.#'),
    )
    CELERY_DEFAULT_EXCHANGE = 'test'
    CELERY_DEFAULT_ROUTING_KEY = 'test.default'
    CELERY_ROUTES = {'giga_web.tasks.conirm_donation': {'queue': 'test-donation_confirms', 'routing_key': 'test.confirm'},
                     'giga_web.tasks.update_project_post': {'queue': 'test-update_project', 'routing_key': 'test.project'},
                     'giga_web.tasks.update_campaign_post': {'queue': 'test-update_campaign', 'routing_key': 'test.campaign'},
                     'giga_web.tasks.update_leaderboard_post': {'queue': 'test-update_leaderboard', 'routing_key': 'test.leaderboard'}
                     }


class TestingConfig(Config):
    TESTING = True
