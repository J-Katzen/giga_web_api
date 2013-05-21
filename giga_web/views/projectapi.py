# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get
import json


class ProjectAPI(MethodView):

    def get(self, proj_id):
        if id is None:
            pass
        else:
            path = '/projects/'
            proj = generic_get(path, proj_id)
            return json.dumps(proj.content)

    def post(self):
        pass

    def delete(self, user_id):
        pass
