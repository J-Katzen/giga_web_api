# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from flask.views import MethodView
from flask import request
import requests
import json
import bcrypt


class ClientUserAPI(MethodView):
    path = '/client_users/'

    def get(self, id, cid=None):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            user = helpers.generic_get(self.path, id)
            return user.content

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            user = helpers.generic_get(self.path, id)
            user_j = user.json()
            data['_id'] = id
            if 'verify_hash' in data:
                if user_j['verify_hash'] == data['verify_hash']:
                    data['verified'] = True
            if 'pw' in data:
                data['pw'] = bcrypt.hashpw(data['pw'], bcrypt.gensalt())
            patched = helpers.generic_patch(self.path, data, user_j['etag'])
            if 'error' in patched:
                return json.dumps(patched)
            else:
                if 'verified' in data:
                    if data['verified']:
                        #send out verified email or password change email
                        pass
                return patched.content
        else:
            data['email'] = data['email'].lower()
            r = requests.get(crud_url + self.path,
                             params={'where': '{"email":"%s"}' % data['email']})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    if 'pw' in data:
                        data['pw'] = bcrypt.hashpw(data['pw'], bcrypt.gensalt())
                    data['verified'] = False
                    data['verify_hash'] = helpers.b64_hash_url(data['email'])
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})
                    if reg.status_code == requests.codes.ok:
                        # send new user email
                        pass
                    return reg.content
                else:
                    return json.dumps({'error': 'User exists'})
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
