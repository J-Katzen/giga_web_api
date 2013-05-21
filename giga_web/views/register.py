# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url
import requests
import bcrypt
import json

app = giga_web


@app.route("/register/user", methods=['POST'])
def register_user():
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


@app.route("/register/client")
def register_client():
    pass


@app.route("/register/c_user")
def register_client_user():
    pass
