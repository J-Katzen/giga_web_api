# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web
from giga_web.tasks import info_mail, mail_list_reg
import json

app = giga_web

@app.route('/info_email/', methods=['POST'])
def informational_email():
	form_data = request.get_json(force=True, silent=False)
	info_mail.delay(form_data, form_data['email'])
	res = {'data': {'status': 'OK', 'message': 'Info request received'}}
	return json.dumps(res)

# @app.route('/mailing_list/<email_list_id>', methods=['POST'])
# def reg_email_list(email_list_id):
# 	form_data = request.get_json(force=True, silent=False)
# 	mail_list_reg.delay(email_list_id, form_data['email'].lower())
# 	return '0'
