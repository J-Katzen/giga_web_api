from kombu import Queue, Exchange
import urllib


class Config(object):
    DEBUG = False
    TESTING = False
    BROKER_URL = 'sqs://%s:%s@' % (urllib.quote('', safe=''),
                                   urllib.quote('', safe=''))
    CELERY_IMPORTS = ('giga_web.tasks')
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'America/New_York'
    BOTO_REGION = 'us-east-1'
    GIGA_NO_REPLY = 'no-reply@gigawatt.co'
    GIGA_VERIFY_HASH_SALT = 'BjunHqx3TnyscBxVfyW0wA=='
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

class ProductionConfig(Config):
    DEBUG = False
    MONGODB_SETTINGS = {
        "DB": "giga_db",
        "HOST": "mongodb://giga:back2future@ec2-54-211-73-122.compute-1.amazonaws.com:27017,ec2-23-22-148-116.compute-1.amazonaws.com:27017,ec2-50-19-60-4.compute-1.amazonaws.com:27017/giga_db?replicaSet=Prod_RS0"
    }
    CELERY_DEFAULT_QUEUE = 'prod'
    CELERY_QUEUES = (
        Queue('prod-donation_confirms', Exchange('prod-donation_confirms'), routing_key='prod.confirm'),
        Queue('prod-update_project', Exchange('prod-update_project'), routing_key='prod.project'),
        Queue('prod-update_campaign', Exchange('prod-update_campaign'), routing_key='prod.campaign'),
        Queue('prod-update_leaderboard', Exchange('prod-update_leaderboard'), routing_key='prod.leaderboard'),
        Queue('prod-update_user', Exchange('prod-update_user'), routing_key='prod.user'),
        Queue('prod-update_ref_user', Exchange('prod-update_ref_user'), routing_key='prod.ref_user'),
        Queue('prod-new_user_mail', Exchange('prod-new_user_mail'), routing_key='prod.mail.new_user'),
        Queue('prod-verified_mail', Exchange('prod-verified_mail'), routing_key='prod.mail.verified_user'),
        Queue('prod-info_mail', Exchange('prod-info_mail'), routing_key='prod.mail.info_mail'),
        Queue('prod-thank_you_mail', Exchange('prod-thank_you_mail'), routing_key='prod.mail.thank_you_mail'),
        Queue('prod-rmc_mail', Exchange('prod-rmc_mail', routing_key='prod.mail.rmc_mail'))
    )
    CELERY_DEFAULT_EXCHANGE = 'prod'
    CELERY_DEFAULT_ROUTING_KEY = 'prod.default'
    CELERY_ROUTES = {'giga_web.tasks.confirm.confirm_donation': {'queue': 'prod-donation_confirms', 'routing_key': 'prod.confirm'},
                     'giga_web.tasks.confirm.update_project_post': {'queue': 'prod-update_project', 'routing_key': 'prod.project'},
                     'giga_web.tasks.confirm.update_campaign_post': {'queue': 'prod-update_campaign', 'routing_key': 'prod.campaign'},
                     'giga_web.tasks.confirm.update_leaderboard_post': {'queue': 'prod-update_leaderboard', 'routing_key': 'prod.leaderboard'},
                     'giga_web.tasks.confirm.update_user_post': {'queue': 'prod-update_user', 'routing_key': 'prod.user'},
                     'giga_web.tasks.confirm.update_ref_user_post': {'queue': 'prod-update_ref_user', 'routing_key': 'prod.ref_user'},
                     'giga_web.tasks.mailer.new_user_mail': {'queue': 'prod-new_user_mail', 'routing_key': 'prod.mail.new_user'},
                     'giga_web.tasks.mailer.verified_mail': {'queue': 'prod-verified_mail', 'routing_key': 'prod.mail.verified_user'},
                     'giga_web.tasks.mailer.thank_you_mail': {'queue': 'prod-thank_you_mail', 'routing_key': 'prod.mail.thank_you_mail'},
                     'giga_web.tasks.mailer.info_mail': {'queue': 'prod-info_mail', 'routing_key': 'prod.mail.info_mail'},
                     'giga_web.tasks.mailer.rmc_email': {'queue': 'prod-rmc_mail', 'routing_key': 'prod.mail.rmc_mail'}
                    }
    CELERY_DEFAULT_RATE_LIMIT = '5/s'


class TestConfig(Config):
    DEBUG = True
    SECRET_KEY = '\x9b\xc9M\xf8\xc5\xc3]8N9p\x00\xc8\x86\xec\x88w\x02\xd3\x0e\xb3)\xd0\x98'
    MONGODB_SETTINGS = {
        "DB": "giga_db",
        "HOST": "mongodb://giga:thefuture@ec2-107-20-187-59.compute-1.amazonaws.com:27017/giga_db"
    }
    CELERY_DEFAULT_QUEUE = 'test'
    CELERY_QUEUES = (
        Queue('test-donation_confirms', Exchange('test-donation_confirms'), routing_key='test.confirm'),
        Queue('test-update_project', Exchange('test-update_project'), routing_key='test.project'),
        Queue('test-update_campaign', Exchange('test-update_campaign'), routing_key='test.campaign'),
        Queue('test-update_leaderboard', Exchange('test-update_leaderboard'), routing_key='test.leaderboard'),
        Queue('test-update_user', Exchange('test-update_user'), routing_key='test.user'),
        Queue('test-new_user_mail', Exchange('test-new_user_mail'), routing_key='test.mail.new_user'),
        Queue('test-thank_you_mail', Exchange('test-thank_you_mail'), routing_key='test.mail.thank_you_mail'),
        Queue('test-info_mail', Exchange('test-info_mail'), routing_key='test.mail.info_mail'),
        Queue('test-verified_mail', Exchange('test-verified_mail'), routing_key='test.mail.verified_user'),
        Queue('test-rmc_mail', Exchange('test-rmc_mail', routing_key='test.mail.rmc_mail'))
    
    )
    CELERY_DEFAULT_EXCHANGE = 'test'
    CELERY_DEFAULT_ROUTING_KEY = 'test.default'
    CELERY_ROUTES = {'giga_web.tasks.confirm.confirm_donation': {'queue': 'test-donation_confirms', 'routing_key': 'test.confirm'},
                     'giga_web.tasks.confirm.update_project_post': {'queue': 'test-update_project', 'routing_key': 'test.project'},
                     'giga_web.tasks.confirm.update_campaign_post': {'queue': 'test-update_campaign', 'routing_key': 'test.campaign'},
                     'giga_web.tasks.confirm.update_leaderboard_post': {'queue': 'test-update_leaderboard', 'routing_key': 'test.leaderboard'},
                     'giga_web.tasks.confirm.update_user_post': {'queue': 'test-update_user', 'routing_key': 'test.user'},
                     'giga_web.tasks.mailer.new_user_mail': {'queue': 'test-new_user_mail', 'routing_key': 'test.mail.new_user'},
                     'giga_web.tasks.mailer.thank_you_mail': {'queue': 'test-thank_you_mail', 'routing_key': 'test.mail.thank_you_mail'},
                     'giga_web.tasks.mailer.info_mail': {'queue': 'test-info_mail', 'routing_key': 'test.mail.info_mail'},
                     'giga_web.tasks.mailer.verified_mail': {'queue': 'test-verified_mail', 'routing_key': 'test.mail.verified_user'},
                     'giga_web.tasks.mailer.rmc_email': {'queue': 'test-rmc_mail', 'routing_key': 'test.mail.rmc_mail'}
                     }
    CELERY_DEFAULT_RATE_LIMIT = '5/s'

