# -*- coding: utf-8 -*-
from giga_web import celery, celery_logger, helpers
from giga_web import Lock, LockTimeout
from giga_web.ext import SES_Mailer

logger = celery_logger


@celery.task
def feedback_mail(name, email, message):
    mailer = SES_Mailer()
    logger.info('task feedback_mail called: args: %s %s %s' % (name, email, message))
    res = mailer.send_feedback_mail(email, name, message)
    if 'error' in res:
        feedback_mail.delay(name, email, message)
    return


@celery.task
def new_user_mail(email, hash, id, name=''):
    mailer = SES_Mailer()
    logger.info('task new_user_mail called: args: %s %s %s %s' % (email, hash, name, id))
    res = mailer.send_new_user(email, hash, id, name)
    if 'error' in res:
        new_user_mail.delay(email, hash, id, name)
    return


@celery.task
def verified_mail(email, share, name=''):
    mailer = SES_Mailer()
    logger.info('task verified_email called: args: %s %s %s' % (email, name, share))
    res = mailer.send_verified_email(email, share, name)
    if 'error' in res:
        verified_mail.delay(email, share, name)
    return

@celery.task
def info_mail(form_info, email):
    mailer = SES_Mailer()
    logger.info('task info_email called: args: %s' % (email))
    res = mailer.send_info_mail(form_info)
    if 'error' in res:
        info_mail.delay(form_info)
    return

@celery.task
def mail_list_reg(email_list_id, email_address):
    mailer = SES_Mailer()
    logger.info('task mail_list_reg called: args: %s %s' % (email_list_id, email_address))
    try:
        with Lock('el_' + email_list_id):
            p = helpers.generic_get('/email_lists/', email_list_id)
            pj = p.json()
            email_idx = helpers.get_index(pj['emails'], 'address', email_address)
            if email_idx is None:
                pj['emails'].append({'address': email_address})
            try:
                upd_list = helpers.generic_patch('/email_lists/', pj, pj['etag'])
            except:
                mail_list_reg.delay(email_list_id, email_address)
                return
            if 'error' in upd_list:
                mail_list_reg.delay(email_list_id, email_address)
    except:
        mail_list_reg.delay(email_list_id, email_address)
    res = mailer.confirm_subscription(email_address)
    if 'error' in res:
        mail_list_reg.delay(email_list_id, email_address)
    return
