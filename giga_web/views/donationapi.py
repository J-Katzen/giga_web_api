# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from giga_web.tasks import confirm_donation
from flask.views import MethodView
from flask import request
from operator import itemgetter
import json
import requests


class DonationAPI(MethodView):
    path = '/donations/'

    def get(self, id, cid=None):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            leaderboard = helpers.generic_get(self.path, id)
            return leaderboard.content

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            # wait - why do we ever patch a donation? refunds? what else?
            pass
        else:
            payload = {'data': data}
            reg = requests.post(crud_url + self.path,
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            # update project(s)
            if 'confirmed' in data:
                confirm_donation.delay(data)
            return reg.content


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
                return r.content
