import boto.ses
import time
from flask import current_app, render_template


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
        if sent24 >= max24:
            return False
        return True

    def _send(self, template, email, title, **args):
        if self._check_limit():
            try:
                res = self.conn.send_email(
                	'Gigawatt <%s>' % (current_app.config.get('GIGA_NO_REPLY')),
                    title,
                    render_template(template, args, email=email),
                    [email, 'jacob.katzen@gigawatt.co'])
                return res
            except:
                return {'error': 'could not send'}
        else:
            return {'error': 'over-rate-limit'}

    def send_new_user(self, email, hash, name):
        return self._send('new_user.html',
                          email,
                          'Verify Your Account!',
                          hash=hash,
                          name=name)

    def send_verified_email(self, email, name):
        return self._send('verified_user.html',
                          email,
                          'Thanks for verifying!',
                          name=name)
