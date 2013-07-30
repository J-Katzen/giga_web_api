import urllib

class Config(object):
    DEBUG = False
    TESTING = False
    CELERY_BROKER_URL = 'sqs://%s:%s@' % (urllib.quote('AKIAJXUZNWCYS2DR7FNQ', safe=''),
                                          urllib.quote('cS7aurMhMikyk9/8y43UPQSnne5Zva+JuF1xPqgL', safe=''))
    CELERY_IMPORTS = ('giga_web.tasks',)
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'America/New_York'


class ProductionConfig(Config):
    DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
