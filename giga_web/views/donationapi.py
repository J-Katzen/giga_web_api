# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
from helpers import generic_get, generic_delete, create_dict_from_form
import json
import requests

class DonationAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/donations/'
            leaderboard = generic_get(path, id)
            return json.dumps(leaderboard.content)

    def post(self, id=None):
        if id is not None:
            pass
        else:
            data = create_dict_from_form(request.form)
            r = requests.get(crud_url + '/leaderboards/',
                             params={'where': '{"camp_id":"' + data['camp_id'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + '/client_users/',
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
            r = generic_delete('/leaderboards/', id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
