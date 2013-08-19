# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from giga_web.tasks import new_user_mail, verified_mail
from flask.views import MethodView
from flask import request
import requests
import json
import bcrypt


class UserAPI(MethodView):
    path = '/users/'

    def get(self, id):
        if id is None:
            return json.dumps({'error': 'no id provided'})
        else:
            user = helpers.generic_get(self.path, id)
            if user.status_code == requests.codes.ok:
                user_j = user.json()
                user_j['share_id'] = helpers.baseconvert(user_j['_id'], helpers.BASE16, helpers.BASE62)
                return json.dumps(user_j)
            else:
                return user

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
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
                name = ''
                if 'firstname' in user_j:
                    name = user_j['firstname']
                if 'lastname' in user_j:
                    name += user_j['lastname']
                if 'verified' in data:
                    if data['verified']:
                        verified_mail.delay(user_j['email'], name)
                return patched.content
        else:
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
                        name = ''
                        if 'firstname' in data:
                            name = data['firstname']
                        if 'lastname' in data:
                            name += ' ' + data['lastname']
                        reg_j = reg.json()
                        new_user_mail.delay(data['email'], data['verify_hash'], reg_j['data']['_id'], name)
                    return reg.content
                else:
                    return json.dumps({'error': 'Email exists'})
            else:
                return json.dumps({'error': 'Could not query DB'})

    def delete(self, user_id):
        if user_id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = helpers.generic_delete(self.path, user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return r.content
