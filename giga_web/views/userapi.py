# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
from helpers import generic_get
import requests
import json
import bcrypt

class UserAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/users/'
            user = generic_get(path, id)
            return json.dumps(user.content)

    def post(self):
        email = (request.form['email']).lower()
        pw = request.form['pw']
        r = requests.get(crud_url + '/users/',
                         params={'where': '{"email":"' + email + '"}'})
        if r.status_code == requests.codes.ok:
            res = r.json()
            if len(res['_items']) == 0:
                crypted = bcrypt.hashpw(pw, bcrypt.gensalt())
                payload = {'data': {
                           'email': email,
                           'pw': crypted,
                           'fb_login': False,
                           't_login': False}}
                reg = requests.post(crud_url + '/users/',
                                    data=json.dumps(payload),
                                    headers={'Content-Type': 'application/json'})

                return json.dumps(reg.content)
            else:
                return json.dumps({'error': 'User exists'})
        else:
            return json.dumps({'error': 'Could not query DB'})

    def delete(self, user_id):
        pass
