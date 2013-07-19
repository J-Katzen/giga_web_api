# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import requests
import json
import bcrypt


class ClientAPI(MethodView):
    path = '/clients/'

    def get(self, id):
        if id is None:
            return json.dumps({'error': 'no id or name provided'})
        else:
            client = helpers.generic_get(self.path, id)
            return client.content

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            data['_id'] = id
            patched = helpers.generic_patch(self.path, data, data['etag'])
            if 'error' in patched:
                return json.dumps(patched)
            else:
                return patched.content
        else:
            r = requests.get(crud_url + self.path,
                             params={'where': '{"name":"' + data['name'] + '"}'})
            r2 = requests.get(crud_url + self.path + data['perma_name'])
            if (r.status_code == requests.codes.ok) and (r2.status_code == 404):
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return reg.content
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
            r = helpers.generic_delete(self.path, id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return r.content
