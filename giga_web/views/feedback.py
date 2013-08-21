# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, helpers
from giga_web.tasks import feedback_mail

app = giga_web

app.route('/leave_feedback/', methods=['POST'])
def feedback_email():
	form_data = helpers.create_dict_from_form(request.form)
	feedback_mail.delay(form_data['name'], form_data['email'], form_data['description'])
	return '0'
