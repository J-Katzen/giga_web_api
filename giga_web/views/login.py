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


@app.route("/<client_perma>/login/", methods=['POST'])
def client_login(client_perma):
    data = helpers.create_dict_from_form(request.form)
    # get client
    client = helpers.generic_get('/clients/', client_perma)
    # get client_user
    if 'error' in client:
        return json.dumps({'error': 'Could not locate client? - contact DBA'})
    else:
        client_user = helpers.generic_get(
            '/client_users/', json.loads(client)['_id'])
        if 'error' in client_user:
            return json.dumps({'error': 'Could not get client_user'})
        else:
            cu_j = client_user.json()
            hashed = cu_j['_items'][0]['pw']
            if bcrypt.hashpw(data['pw'], hashed) == hashed:
                return json.dumps(res['_items'][0])
            else:
                return json.dumps({'error': 'Invalid password'})
