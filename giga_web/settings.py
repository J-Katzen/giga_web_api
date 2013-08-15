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
    BOTO_REGION = 'us-east-1'
    GIGA_NO_REPLY = 'no-reply@gigawatt.co'
    GIGA_VERIFY_HASH_SALT = '\xf6\x0c\xbbL\xd7\\J\xc3\xa8$\x17\xb5\x03\x90\x14X'
    AWS_ACCESS_KEY_ID = 'AKIAIK3ONM7NVRHJXINA'
    AWS_SECRET_ACCESS_KEY = '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'

class ProductionConfig(Config):
    DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS = 'ec2-54-226-128-157.compute-1.amazonaws.com'
    REDIS_PORT = 6379
    REDIS_DB = 1
    CELERY_DEFAULT_QUEUE = 'test'
    CELERY_QUEUES = (
        Queue('test-donation_confirms', Exchange('test-donation_confirms'), routing_key='test.confirm'),
        Queue('test-update_project', Exchange('test-update_project'), routing_key='test.project'),
        Queue('test-update_campaign', Exchange('test-update_campaign'), routing_key='test.campaign'),
        Queue('test-update_leaderboard', Exchange('test-update_leaderboard'), routing_key='test.leaderboard'),
        Queue('test-new_user_mail', Exchange('test-new_user_mail'), routing_key='test.mail.new_user'),
        Queue('test-verified_mail', Exchange('test-verified_mail'), routing_key='test.mail.verified_user')
    
    )
    CELERY_DEFAULT_EXCHANGE = 'test'
    CELERY_DEFAULT_ROUTING_KEY = 'test.default'
    CELERY_ROUTES = {'giga_web.tasks.confirm.confirm_donation': {'queue': 'test-donation_confirms', 'routing_key': 'test.confirm'},
                     'giga_web.tasks.confirm.update_project_post': {'queue': 'test-update_project', 'routing_key': 'test.project'},
                     'giga_web.tasks.confirm.update_campaign_post': {'queue': 'test-update_campaign', 'routing_key': 'test.campaign'},
                     'giga_web.tasks.confirm.update_leaderboard_post': {'queue': 'test-update_leaderboard', 'routing_key': 'test.leaderboard'},
                     'giga_web.tasks.mailer.new_user_mail': {'queue': 'test-new_user_mail', 'routing_key': 'test.mail.new_user'},
                     'giga_web.tasks.mailer.verified_mail': {'queue': 'test-verified_mail', 'routing_key': 'test.mail.verified_user'}
                     }


class TestingConfig(Config):
    TESTING = True
