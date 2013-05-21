# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get
import json


class CampaignAPI(MethodView):

    def get(self, campaign_perma):
        if id is None:
            pass
        else:
            path = '/campaigns/'
            camp = generic_get(path, campaign_perma)
            return json.dumps(camp.content)

    def post(self):
        pass

    def delete(self, user_id):
        pass
