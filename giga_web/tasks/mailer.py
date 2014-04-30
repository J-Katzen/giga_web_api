# -*- coding: utf-8 -*-
from giga_web import celery, celery_logger, helpers, mailer
from giga_web.ext import Lock, LockTimeout
import time

logger = celery_logger

# pledge signup for the future - maconday signup for right now
@celery.task
def macon_signup(email):
    logger.info('task macon_signup called: args: %s' % (email))
    res = mailer.send_pledge(email)
    if 'error' in res:
        time.sleep(.2)
        macon_signup.delay(email)
    return

@celery.task
def new_user_mail(email, hash, id, name=''):
    logger.info('task new_user_mail called: args: %s %s %s %s' % (email, hash, name, id))
    res = mailer.send_new_user(email, hash, id, name)
    if 'error' in res:
        time.sleep(.2)
        new_user_mail.delay(email, hash, id, name)
    return


@celery.task
def verified_mail(email, share, name=''):
    logger.info('task verified_email called: args: %s %s %s' % (email, name, share))
    res = mailer.send_verified_email(email, share, name)
    if 'error' in res:
        time.sleep(.2)
        verified_mail.delay(email, share, name)
    return

@celery.task
def thank_you_mail(email, project_id):
    logger.info('task thank_you_mail called: args: %s %s' % (email, project_id))
    res = mailer.thankyou_email(email, project_id)
    if 'error' in res:
        time.sleep(.2)
        thank_you_mail.delay(email, project_id)
    return

@celery.task
def rmc_email(email, project_id):
    logger.info('task rmc_email called: args: %s %s' % (email, project_id))
    res = mailer.rmc_thanks(email, project_id)
    if 'error' in res:
        time.sleep(.2)
        rmc_email.delay(email, project_id)
    return


@celery.task
def info_mail(form_info, email):
    logger.info('task info_email called: args: %s' % (email))
    res = mailer.send_info_mail(form_info)
    if 'error' in res:
        time.sleep(.2)
        info_mail.delay(form_info)
    return
