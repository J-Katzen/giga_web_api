# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web
import requests

app = giga_web

# unique_email check


@app.route("/unique_email/", methods=['GET'])
def account_email_check():
    email = request.args['email']
    r = requests.get(crud_url + '/users/',
                     params={'where': '{"email":"' + str(email).lower() + '"}'})
    if r.status_code == requests.codes.ok:
        res = r.json()
        if len(res['_items']) > 0:
            return '1'
        else:
            return '0'
    else:
        return '-1'
