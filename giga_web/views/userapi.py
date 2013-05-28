# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
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
            return json.dumps(user.content)

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            data['_id'] = id
            patched = helpers.generic_patch(self.path, data)
            if 'error' in patched:
                return patched
            else:
                return json.dumps(patched.content)
        else:
            data['fb_login'] = False
            data['t_login'] = False
            r = requests.get(crud_url + self.path,
                             params={'where': '{"email":"' + data['email'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    data['pw'] = bcrypt.hashpw(data['pw'], bcrypt.gensalt())
                    print data
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'User exists'})
            else:
                return json.dumps({'error': 'Could not query DB'})

    def delete(self, user_id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = helpers.generic_delete(self.path, user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
