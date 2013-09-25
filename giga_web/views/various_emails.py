# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web
from giga_web.tasks import info_mail

app = giga_web

@app.route('/info_email/', methods=['POST'])
def informational_email():
	form_data = request.get_json(force=True, silent=False)
	info_mail.delay(form_data, form_data['email'])
	return '0'
