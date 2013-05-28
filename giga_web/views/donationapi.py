# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import json
import requests


class DonationAPI(MethodView):
    path = '/donations/'

    def get(self, cid, id):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            leaderboard = helpers.generic_get(self.path, id)
            return json.dumps(leaderboard.content)

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            pass
        else:

            payload = {'data': data}
            reg = requests.post(crud_url + self.path,
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            # update project
            # update campaign
            # update leaderboard
            return json.dumps(reg.content)

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            # update project
            # update campaign
            # update leaderboard
            r = helpers.generic_delete(self.path, id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
