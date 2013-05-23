# -*- coding: utf-8 -*-

from flask.views import MethodView
from projectapi import ProjectAPI
from leaderboardapi import LeaderboardAPI
from flask import request
from helpers import generic_get, generic_delete
import json


class CampaignAPI(MethodView):

    def get(self, campaign_perma, cid=None):
        if campaign_perma is None:
            pass
        else:
            path = '/campaigns/'
            camp = generic_get(path, campaign_perma)
            return json.dumps(camp.content)

    def post(self, id=None, cid=None):
        pass

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            camp = generic_get(path, id)
            res = camp.json()
            for proj in res['project_list']:
                d = generic_delete('/projects/', proj['p_id'])
            r = generic_delete('/campaigns/', user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
