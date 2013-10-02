# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from flask.views import MethodView
from flask import request
import json
import requests


class LeaderboardAPI(MethodView):
    path = '/leaderboards/'

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
            data['_id'] = id
            patched = helpers.generic_patch(self.path, data, data['etag'])
            if 'error' in patched:
                return json.dumps(patched)
            else:
                return patched.content
        else:
            data['class_yr_totals'] = []
            r = requests.get(crud_url + self.path,
                             params={'where': '{"camp_id":"' + data['camp_id'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return reg.content
                else:
                    return json.dumps({'error': 'Leaderboard exists for this campaign'})
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
