# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url
import helpers
import requests
import bcrypt
import json

app = giga_web

# login


@app.route("/register/", methods=['POST'])
def register():
    data = helpers.create_dict_from_form(request.form)
    r = requests.get(crud_url + '/users/',
                     params={'where': '{"email":"' + data['email'] + '"}'})
    if r.status_code == requests.codes.ok:
        res = r.json()
        if len(res['_items']) > 0:
            return json.dumps({'error': 'This email is already registered'})
        else:
            hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
            data.pop('password', None)
            data['pw'] = hashed
            payload = {'data': data}
            reg = requests.post(crud_url + '/users/',
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            return reg.content
    else:
        return json.dumps({'error': 'Could not query DB'})


@app.route("/<client_perma>/register/", methods=['POST'])
def client_register(client_perma):
    data = helpers.create_dict_from_form(request.form)
    client = helpers.generic_get('/clients/', client_perma)
    if 'error' in client:
        return json.dumps({'error': 'Could not locate client? - contact DBA'})
    client_pj = client.json()
    r = requests.get(crud_url + '/client_users/',
                     params={'where': '{"email":"%s","client_id":"%s"}' % (data['email'], client_pj['_id'])})
    res = r.json()
    if len(res['_items']) > 0:
        return json.dumps({'error': 'This email already registered for this client'})
    hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    data.pop('password', None)
    data['pw'] = hashed
    data['client_id'] = client_pj['_id']
    payload = {'data': data}
    reg = requests.post(crud_url + '/users/',
                        data=json.dumps(payload),
                        headers={'Content-Type': 'application/json'})
    return reg.content
