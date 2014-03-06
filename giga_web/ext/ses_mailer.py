import boto.ses
import sys
import os
from flask import current_app, render_template

class SES_Mailer(object):

    def __init__(self, app=None):
        """
        SES Mailer Class

        """
        self.app = app
        if app is not None:
            self.conn = boto.ses.connect_to_region(
                app.config['BOTO_REGION'],
                aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

    def _check_limit(self):
        quota = self.conn.get_send_quota()
        max24 = quota['GetSendQuotaResponse']['GetSendQuotaResult']['Max24HourSend']
        sent24 = quota['GetSendQuotaResponse']['GetSendQuotaResult']['SentLast24Hours']
        if int(float(sent24)) >= int(float(max24)):
            return False
        return True

    def _send(self, template, email, title, **args):
        try:
            res = self.conn.send_email(
                'Gigawatt <%s>' % (current_app.config.get('GIGA_NO_REPLY')),
                title,
                render_template(template, **args),
                email,
                bcc_addresses=[],
                format='html')
            return res
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {'error': 'could not send', 'other_1': exc_type, 'other_2': fname, 'other_3': exc_tb.tb_lineno}

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
        form_info.pop('email')
        self._send('info_thanks.html',
                   [form_info['uemail']],
                   '%s - Thanks for contacting Gigawatt!' % (form_info['name']),
                    **form_info)
        return self._send('info_email.html',
                          ['founders@gigawatt.co'],
                          'Info Request from %s' % (form_info['name']),
                          **form_info)

    def thankyou_email(self, email, project_id):
        data = {'uemail': email, 'project_id': project_id}
        return self._send('thankyou_mail.html',
                          [email],
                          'Thanks for your gift to Blitz Day (your special link is included!)',
                          **data)

    def confirm_subscription(self, email):
        context = {}
        return self._send('subscription_confirm.html',
                          [email],
                          'Get Excited for Muhlenberg\'s Day of Giving Campaign!',
                          **context)

    def lehigh_initial_gift(self, donation, share):
      context = {'share_id': share}
      return self._send('lehigh_initial_gift.html',
                        [donation['email']],
                        'Thanks for your gift to the #Lehigh5000 Challenge!',
                        **context)

    def lehigh_update(self, ref_user, share, count):
      context = {'share_id': share,
                 'ref_count': count}
      return self._send('lehigh_ref_update.html',
                        [ref_user['email']],
                        'Someone used your #Lehigh5000 Challenge link!',
                        **context)

    def lehigh_winner(self, ref_user, share, count):
      context = {'share_id': share,
                 'ref_count': count,
                 'donor_email': ref_user['email'],
                 'donor_name': ref_user['fullname']}
      self._send('share_winner.html',
                 ['jacob.katzen@gigawatt.co','jake@gigawatt.co','greg@gigawatt.co'],
                 'A winner based on shares has been made!',
                 **context)
      return self._send('lehigh_ref_winner.html',
                        [ref_user['email']],
                        'Hooray! You\'re getting a Secret Prize from the #Lehigh5000 Challenge!',
                        **context)
