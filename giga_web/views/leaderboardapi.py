# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get
import json


class LeaderboardAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/leaderboards/'
            leaderboard = generic_get(path, id)
            return json.dumps(leaderboard.content)

    def post(self):
        pass

    def delete(self, user_id):
        pass
