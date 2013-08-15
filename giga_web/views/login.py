# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url, helpers
import requests
import bcrypt
import json

app = giga_web

# login


@app.route("/login/", methods=['POST'])
def login():
    data = helpers.create_dict_from_form(request.form)
    print data
    r = requests.get(crud_url + '/users/',
                     params={'where': '{"email":"' + data['email'] + '"}'})
    if r.status_code == requests.codes.ok:
        res = r.json()
        if len(res['_items']) > 0:
            hashed = res['_items'][0]['pw']
            if bcrypt.hashpw(data['password'], hashed) == hashed:
                return json.dumps(res['_items'][0])
            else:
                return json.dumps({'error': 'Invalid password'})
        else:
            return json.dumps({'error': 'No user registered with this email'})
    else:
        return json.dumps({'error': 'Could not query DB'})


@app.route("/unique_email/", methods=['GET'])
def account_email_check():
    email = request.args['email']
    print email
    r = requests.get(crud_url + '/users/',
                     params={'where': '{"email":"' + str(email) + '"}'})
    if r.status_code == requests.codes.ok:
        res = r.json()
        if len(res['_items']) > 0:
            return '1'
        else:
            return '0'
    else:
        return '-1'



@app.route("/<client_perma>/login/", methods=['POST'])
def client_login(client_perma):
    data = helpers.create_dict_from_form(request.form)
    # get client
    client = helpers.generic_get('/clients/', client_perma)
    # get client_user
    if 'error' in client:
        return json.dumps({'error': 'Could not locate client? - contact DBA'})
    else:
        client_pj = client.json()
        client_user = requests.get(crud_url + '/client_users/',
                                   params={'where': '{"email":"%s","client_id":"%s"}' % (data['email'], client_pj['_id'])})
        if 'error' in client_user:
            return json.dumps({'error': 'Could not get client_user'})
        else:
            cu_j = client_user.json()
            hashed = cu_j['_items'][0]['pw']
            if bcrypt.hashpw(data['password'], hashed) == hashed:
                return json.dumps(cu_j['_items'][0])
            else:
                return json.dumps({'error': 'Invalid password'})
