# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import requests
import json
import bcrypt


class ClientUserAPI(MethodView):
    path = '/client_users/'

    def get(self, cid, id):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            user = helpers.generic_get(self.path, id)
            return json.dumps(user.content)

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            pass
        else:
            r = requests.get(crud_url + self.path,
                             params={'where': '{"uname":"' + data['uname'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    data['pw'] = bcrypt.hashpw(data['pw'], bcrypt.gensalt())
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
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
                return json.dumps(r.content)