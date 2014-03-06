# -*- coding: utf-8 -*-
from giga_web import celery, celery_logger, helpers, mailer
from giga_web.ext import Lock, LockTimeout

logger = celery_logger

@celery.task
def new_user_mail(email, hash, id, name=''):
    logger.info('task new_user_mail called: args: %s %s %s %s' % (email, hash, name, id))
    res = mailer.send_new_user(email, hash, id, name)
    if 'error' in res:
        new_user_mail.delay(email, hash, id, name)
    return


@celery.task
def verified_mail(email, share, name=''):
    logger.info('task verified_email called: args: %s %s %s' % (email, name, share))
    res = mailer.send_verified_email(email, share, name)
    if 'error' in res:
        verified_mail.delay(email, share, name)
    return

@celery.task
def thank_you_mail(email, project_id):
    logger.info('task thank_you_mail called: args: %s %s' % (email, project_id))
    res = mailer.thankyou_email(email, project_id)
    if 'error' in res:
        thank_you_mail.delay(email, project_id)
    return

@celery.task
def info_mail(form_info, email):
    logger.info('task info_email called: args: %s' % (email))
    res = mailer.send_info_mail(form_info)
    if 'error' in res:
        info_mail.delay(form_info)
    return
