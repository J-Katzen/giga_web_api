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
            return leaderboard.content

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            # wait - why do we ever patch a donation? refunds? what else?
            pass
        else:
            payload = {'data': data}
            reg = requests.post(crud_url + self.path,
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            # update project
            for proj in data['distro']:
                p = helpers.generic_get('/projects/', proj['p_id'])
                pj = p.json()
                pj['raised'] += proj['amt']
                if pj['raised'] >= pj['goal']:
                    pj['completed'] = True
                upd_p = helpers.generic_patch('/projects/', pj)
            # update campaign
            camp = helpers.generic_get('/campaigns/', data['camp_id'])
            camp_j = camp.json()
            lead_id = camp_j['leaderboard_id']
            camp_j['total_raised'] += data['donated']
            if camp_j['total_raised'] >= camp_j['total_goal']:
                camp_j['completed'] = True
            upd_camp = helpers.generic_patch('/campaigns/', camp_j)
            # update leaderboard
            lead = helpers.generic_get('/leaderboards/', lead_id)
            lead_j = lead.json()
            lead_j['raised'] += data['donated']
            if 'ref' in data:
                lead_j['ref'] += data['donated']
                user = next((d for d in lead_j['donors'] if
                             d['email'].lower() == data['ref'].lower()), None)
                if user is not None:
                    user['ref'] += data['donated']
            user2 = next((d for d in lead_j['donors'] if
                          d['email'].lower() == data['email'].lower()), None)
            lead_j['donors'].append({'email': data['email'],
                                     'donated': data['donated'],
                                     'ref': 0})
            upd_lead = helpers.generic_patch('/leaderboards/', lead_j)
            return reg.content

    def update_project(self, )

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
