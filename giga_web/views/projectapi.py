# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get
import json


class ProjectAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/projects/'
            proj = generic_get(path, proj_id)
            return json.dumps(proj.content)

    def post(self, id):
        if id is not None:
            pass  # patch
        else:
            name = request.form['name']
            perma_name = request.form['perma_name']
            giga_fee_percent = request.form['giga_fee_percent']
            giga_fee_cents = request.form['giga_fee_cents']
            trans_fee_percent = request.form['trans_fee_percent']
            trans_fee_cents = request.form['trans_fee_cents']
            r = requests.get(crud_url + '/clients/',
                             params={'where': '{"name":"' + name + '"}'})
            r2 = requests.get(crud_url + '/clients/' + perma_name)
            if (r.status_code == requests.codes.ok) and (r2.status_code == 404):
                res = r.json()
                if len(res['_items']) == 0:
                    crypted = bcrypt.hashpw(pw, bcrypt.gensalt())
                    payload = {'data': {
                               'name': name,
                               'perma_name': perma_name,
                               'giga_fee_percent': giga_fee_percent,
                               'giga_fee_cents': giga_fee_cents,
                               'trans_fee_percent': trans_fee_percent,
                               'trans_fee_cents': trans_fee_cents}}
                    reg = requests.post(crud_url + '/clients/',
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'Client name is not unique'})
            elif r.status_code == r2.status_code == 404:
                return json.dumps({'error': 'Could not query DB'})
            elif r.status_code == r2.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    return json.dumps({'error': 'perma_name not unique'})
                else:
                    return json.dumps({'error': 'name and perma_name not unique'})
            else:
                return json.dumps({'error': 'perma_name not unique'})

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = generic_delete('/projects/', user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
