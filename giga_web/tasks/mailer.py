# -*- coding: utf-8 -*-
from giga_web import celery, celery_logger
from giga_web.ext import SES_Mailer

logger = celery_logger

@celery.task
def new_user_mail(email, hash, name=''):
    mailer = SES_Mailer()
    logger.info('task new_user_mail called: args: %s %s %s' % (email, hash, name))
    res = mailer.send_new_user(email, hash, name)
    if 'error' in res:
        print res
    	new_user_mail.delay(email, hash, name)
    return


@celery.task
def verified_mail(email, name=''):
    mailer = SES_Mailer()
    logger.info('task verified_email called: args: %s %s' % (email, name))
    res = mailer.send_verified_email(email, name)
    if 'error' in res:
    	verified_mail.delay(email, name)
    return
