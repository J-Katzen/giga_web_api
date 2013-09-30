# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from flask.views import MethodView
from flask import request
import requests
import json


class EmailListAPI(MethodView):
    path = '/email_lists/'

    def get(self, id):
        if id is None:
            return json.dumps({'error': 'no id provided'})
        else:
            email_list = helpers.generic_get(self.path, id)
            if email_list.status_code == requests.codes.ok:
                return email_list.content
            return email_list

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
            if 'camp_id' in data:
                related_id = data['camp_id']
                related_text = 'camp_id'
            elif 'proj_id' in data:
                related_id = data['proj_id']
                related_text = 'proj_id'
            elif 'client_id' in data:
                related_id = data['client_id']
                related_text = 'client_id'
            r = requests.get(crud_url + self.path,
                             params={'where': '{"%s": "%s"}' % (related_text, related_id)})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return reg.content
                else:
                    return json.dumps({'error': 'email_list already exists for this %s:%s - delete existing one first' % (related_text, related_id)})
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
