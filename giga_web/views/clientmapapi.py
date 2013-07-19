# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import requests
import json


class ClientMapAPI(MethodView):
    path = '/client_maps/'

    def get(self, id, cid=None):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            c_map = helpers.generic_get(self.path, id)
            return c_map.content

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            data['_id'] = id
            patched = helpers.generic_patch(self.path, data, data['etag'])
            if 'error' in patched:
                return patched
            else:
                return patched.content
        else:
            r = requests.get(crud_url + self.path,
                             params={'where': '{"client_id":"%s"}' % data['client_id']})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return reg.content
                else:
                    return json.dumps({'error': 'client_map already exist for this client_id - delete existing one first'})
            else:
                return json.dumps({'error': 'Could not query DB'})

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = helpers.generic_delete(self.path, id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return r.content
