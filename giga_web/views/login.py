# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url
import helpers
import requests
import bcrypt
import json

app = giga_web

# login

@app.route("/login/", methods=['POST'])
def login():
    data = helpers.create_dict_from_form(request.form)
    r = requests.get(crud_url + '/users/',
                     params={'where': '{"email":"' + data['email'] + '"}'})
    if r.status_code == requests.codes.ok:
        res = r.json()
        hashed = res['_items'][0]['pw']
        if bcrypt.hashpw(data['pw'], hashed) == hashed:
            return json.dumps(res['_items'][0])
        else:
            return json.dumps({'error': 'Invalid password'})
    else:
        return json.dumps({'error': 'Could not query DB'})
