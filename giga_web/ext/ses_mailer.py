import boto.ses
import sys
import os
from flask import current_app, render_template
from giga_web import celery_logger

logger = celery_logger


class SES_Mailer(object):

    def __init__(self):
        """
        SES Mailer Class

        """

        self.conn = boto.ses.connect_to_region(
            current_app.config.get('BOTO_REGION'),
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'))

    def _check_limit(self):
        quota = self.conn.get_send_quota()
        max24 = quota['GetSendQuotaResponse']['GetSendQuotaResult']['Max24HourSend']
        sent24 = quota['GetSendQuotaResponse']['GetSendQuotaResult']['SentLast24Hours']
        if int(float(sent24)) >= int(float(max24)):
            return False
        return True

    def _send(self, template, email, title, **args):
        if self._check_limit():
            try:
                res = self.conn.send_email(
                    'Gigawatt <%s>' % (current_app.config.get('GIGA_NO_REPLY')),
                    title,
                    render_template(template, **args),
                    email,
                    bcc_addresses=[],
                    format='html')
                return res
            except Exception:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                return {'error': 'could not send', 'other_1': exc_type, 'other_2': fname, 'other_3': exc_tb.tb_lineno}
        else:
            return {'error': 'over-rate-limit'}

    def send_new_user(self, email, hash, id, name):
        context = {'hash': hash,
                   'name': name,
                   'user_id': id}
        return self._send('new_user.html',
                          [email],
                          'Verify Your MoCoMotion Account!',
                          **context)

    def send_verified_email(self, email, share, name):
        context = {'name': name,
                   'user_email': email,
                   'share': share}
        return self._send('verified_user.html',
                          [email],
                          'Thanks for verifying with MoCoMotion!',
                          **context)

    def send_info_mail(self, form_info):
        form_info['uemail'] = form_info['email']
        form_info['personType'] = form_info['person-type']
        form_info.pop('person-type', None)
        form_info.pop('email', None)
        return self._send('info_email.html',
                          ['jacob.katzen@gigawatt.co', 'greg@gigawatt.co',
                          'jake@gigawatt.co', 'roger@gigawatt.co', 'tedbrooks2@gmail.com'],
                          'Info Request from %s' % (form_info['name']),
                          **form_info)

    def confirm_subscription(self, email):
        context = {}
        return self._send('subscription_confirm.html',
                          [email],
                          'Get Excited for Muhlenberg\'s Day of Giving Campaign!',
                          **context)
