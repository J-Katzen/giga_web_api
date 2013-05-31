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
            # update project(s)
            for proj in data['distro']:
                up = self.update_project_post(proj)
                if 'error' in up:
                    return up
            # update campaign
            camp, leader_id = self.update_campaign_post(data)
            if 'error' in camp:
                return camp
            # update leaderboard
            lead = self.update_leaderboard_post(data, leader_id)
            if 'error' in lead:
                return lead
            return reg.content

    def update_project_post(self, proj):
        p = helpers.generic_get('/projects/', proj['p_id'])
        pj = p.json()
        pj['raised'] += proj['amt']
        if (pj['type'] == 'rolling') and (pj['raised'] >= pj['goal']):
            pj['completed'] = True
            pj['active'] = False
                # make a new project active:  update campaign and project
        parm = {
            'where': '{"client_id": "%s","active": false}' % pj['camp_id'],
            'sort': '[("votes": -1)]'
        }
        popular_req = requests.get(crud_url + '/projects/', params=parm)
        pop_req_j = popular_req.json()
        pop_proj = pop_req_j['_items'][0]
        pop_proj['active'] = True
        pop_proj_id = pop_proj['_id']
        upd_pop = helpers.generic_patch('/projects/', pop_proj)
        if 'error' not in upd_pop:
            upd_p = helpers.generic_patch('/projects/', pj)
        else:
            upd_p = {'error': 'Could not set new active project'}
        return upd_p, pop_proj_id

    def update_campaign_post(self, data):
        camp = helpers.generic_get('/campaigns/', data['camp_id'])
        camp_j = camp.json()
        lead_id = camp_j['leaderboard_id']
        camp_j['total_raised'] += data['donated']
        if camp_j['total_raised'] >= camp_j['total_goal']:
            camp_j['completed'] = True
        # delete project from active list
        # add the active, but not complete project
        upd_camp = helpers.generic_patch('/campaigns/', camp_j)
        return upd_camp, lead_id

    def update_leaderboard_post(self, data, lead_id):
        lead = helpers.generic_get('/leaderboards/', lead_id)
        lead_j = lead.json()
        lead_j['raised'] += data['donated']
        if 'ref' in data:
            lead_j['referred'] += data['donated']
            # find out if the referral email is in the leaderboard list
            user = next((d for d in lead_j['donors'] if
                         d['email'].lower() == data['ref'].lower()), None)
            # if so, update the stats!
            if user is not None:
                lead_j['donors'] = [d for d in lead_j['donors'] if d[
                    'email'].lower() != data['ref'].lower()]
                user['ref'] += data['donated']
                lead_j['donors'].append(user)
        # check if user donating is already in leaderboard
        user2 = next((d for d in lead_j['donors'] if
                      d['email'].lower() == data['email'].lower()), None)
        if user2 is not None:
            lead_j['donors'] = [d for d in lead_j['donors'] if d[
                'email'].lower() != data['email'].lower()]
            user2['donated'] += data['donated']
            lead_j['donors'].append(user2)
        else:
            lead_j['donors'].append({'email': data['email'].lower(),
                                     'donated': data['donated'],
                                     'ref': 0})
        upd_lead = helpers.generic_patch('/leaderboards/', lead_j)
        return upd_lead

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
