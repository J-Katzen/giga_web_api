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
    GIGA_VERIFY_HASH_SALT = 'BjunHqx3TnyscBxVfyW0wA=='
    AWS_ACCESS_KEY_ID = 'AKIAIK3ONM7NVRHJXINA'
    AWS_SECRET_ACCESS_KEY = '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'

class ProductionConfig(Config):
    DEBUG = False
    REDIS = 'ec2-54-227-124-243.compute-1.amazonaws.com'
    REDIS_PORT = 6379
    REDIS_DB = 1
    CELERY_DEFAULT_QUEUE = 'prod'
    CELERY_QUEUES = (
        Queue('prod-donation_confirms', Exchange('prod-donation_confirms'), routing_key='prod.confirm'),
        Queue('prod-update_project', Exchange('prod-update_project'), routing_key='prod.project'),
        Queue('prod-update_campaign', Exchange('prod-update_campaign'), routing_key='prod.campaign'),
        Queue('prod-update_leaderboard', Exchange('prod-update_leaderboard'), routing_key='prod.leaderboard'),
        Queue('prod-update_user', Exchange('prod-update_user'), routing_key='prod.user'),
        Queue('prod-new_user_mail', Exchange('prod-new_user_mail'), routing_key='prod.mail.new_user'),
        Queue('prod-verified_mail', Exchange('prod-verified_mail'), routing_key='prod.mail.verified_user'),
        Queue('prod-info_mail', Exchange('prod-info_mail'), routing_key='prod.mail.info_mail'),
        Queue('prod-mail_list_reg', Exchange('prod-mail_list_reg'), routing_key='prod.mail.list_reg')
    )
    CELERY_DEFAULT_EXCHANGE = 'prod'
    CELERY_DEFAULT_ROUTING_KEY = 'prod.default'
    CELERY_ROUTES = {'giga_web.tasks.confirm.confirm_donation': {'queue': 'prod-donation_confirms', 'routing_key': 'prod.confirm'},
                     'giga_web.tasks.confirm.update_project_post': {'queue': 'prod-update_project', 'routing_key': 'prod.project'},
                     'giga_web.tasks.confirm.update_campaign_post': {'queue': 'prod-update_campaign', 'routing_key': 'prod.campaign'},
                     'giga_web.tasks.confirm.update_leaderboard_post': {'queue': 'prod-update_leaderboard', 'routing_key': 'prod.leaderboard'},
                     'giga_web.tasks.confirm.update_user_post': {'queue': 'prod-update_user', 'routing_key': 'prod.user'},
                     'giga_web.tasks.mailer.new_user_mail': {'queue': 'prod-new_user_mail', 'routing_key': 'prod.mail.new_user'},
                     'giga_web.tasks.mailer.verified_mail': {'queue': 'prod-verified_mail', 'routing_key': 'prod.mail.verified_user'},
                     'giga_web.tasks.mailer.info_mail': {'queue': 'prod-info_mail', 'routing_key': 'prod.mail.info_mail'},
                     'giga_web.tasks.mailer.mail_list_reg': {'queue': 'prod-mail_list_reg', 'routing_key': 'prod.mail.list_reg'}
                    }


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
        Queue('test-update_user', Exchange('test-update_user'), routing_key='test.user'),
        Queue('test-new_user_mail', Exchange('test-new_user_mail'), routing_key='test.mail.new_user'),
        Queue('test-verified_mail', Exchange('test-verified_mail'), routing_key='test.mail.verified_user')
    
    )
    CELERY_DEFAULT_EXCHANGE = 'test'
    CELERY_DEFAULT_ROUTING_KEY = 'test.default'
    CELERY_ROUTES = {'giga_web.tasks.confirm.confirm_donation': {'queue': 'test-donation_confirms', 'routing_key': 'test.confirm'},
                     'giga_web.tasks.confirm.update_project_post': {'queue': 'test-update_project', 'routing_key': 'test.project'},
                     'giga_web.tasks.confirm.update_campaign_post': {'queue': 'test-update_campaign', 'routing_key': 'test.campaign'},
                     'giga_web.tasks.confirm.update_leaderboard_post': {'queue': 'test-update_leaderboard', 'routing_key': 'test.leaderboard'},
                     'giga_web.tasks.confirm.update_user_post': {'queue': 'test-update_user', 'routing_key': 'test.user'},
                     'giga_web.tasks.mailer.new_user_mail': {'queue': 'test-new_user_mail', 'routing_key': 'test.mail.new_user'},
                     'giga_web.tasks.mailer.verified_mail': {'queue': 'test-verified_mail', 'routing_key': 'test.mail.verified_user'}
                     }


class TestingConfig(Config):
    TESTING = True
