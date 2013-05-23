# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get
import json


class LeaderboardAPI(MethodView):

    def get(self, id, cid=None):
        if id is None:
            pass
        else:
            path = '/leaderboards/'
            leaderboard = generic_get(path, id)
            return json.dumps(leaderboard.content)

    def post(self, id=None, cid=None):
        pass

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = generic_delete('/leaderboards/', user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
