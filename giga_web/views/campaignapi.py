# -*- coding: utf-8 -*-

from giga_web import helpers
from flask.views import MethodView
from flask import request
import json
import requests


class CampaignAPI(MethodView):
    path = '/campaigns/'

    def get(self, campaign_perma, cid=None):
        if campaign_perma is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            camp = helpers.generic_get(self.path, campaign_perma)
            if 'error' not in camp:
                camp = camp.json()
                camp['active_list'] = sorted(camp['active_list'],
                                             key=lambda k: k['raised'],
                                             reverse=True)
            return json.dumps(camp)

    def post(self, campaign_perma=None):
        data = request.get_json(force=True, silent=False)
        if campaign_perma is not None:
            data['_id'] = campaign_perma
            patched = helpers.generic_patch(self.path, data, data['etag'])
            if 'error' in patched:
                return json.dumps(patched)
            else:
                return patched.content
        else:
            data['total_raised'] = 0
            data['total_goal'] = 0
            data['completed'] = False
            data['active_list'] = []
            data['total_donor_ct'] = 0
            data['total_prize'] = 0
            r = requests.get(crud_url + self.path,
                             params={'where': '{"perma_name":"%s"}' % data['perma_name']})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})
                    # create and attach leaderboard
                    reg_j = reg.json()
                    lead_data = {'client_id': data['client_id'],
                                 '_id': reg_j['data']['_id']}
                    cl = self.create_leaderboard(lead_data)
                    if cl['data']['status'] == 'OK':
                        lead_data['leaderboard_id'] = cl['data']['_id']
                        p = helpers.generic_patch(self.path, lead_data, reg_j['data']['etag'])
                        if p.json()['data']['status'] == 'OK':
                            return reg.content
                        else:
                            return json.dumps({'error': 'Leaderboard created but unattached'})
                    else:
                        return json.dumps({'error': 'did not create leaderboard'})
                else:
                    return json.dumps({'error': 'Campaign_perma exists'})
            else:
                return json.dumps({'error': 'Could not query DB'})

    def create_leaderboard(self, camp_data):
        lead = {'client_id': camp_data['client_id'],
                'camp_id': camp_data['_id'],
                'raised': 0,
                'referred': 0,
                'donors': []}
        res = requests.post(crud_url + '/leaderboards/',
                            data=json.dumps({'data': lead}),
                            headers={'Content-Type': 'application/json'})
        return res.json()

    # should we ever really delete a campaign if it's been in motion? date
    # restrictions need to be applied
    def delete(self, campaign_perma):
        if campaign_perma is None:
            return json.dumps({'error': 'did not provide campaign_perma'})
        else:
            camp = helpers.generic_get(self.path, campaign_perma)
            res = camp.json()
            for proj in res['active_list']:
                d = helpers.generic_delete('/projects/', proj['p_id'])
            if 'leaderboard_id' in res:
                lead = helpers.generic_delete('/leaderboards/', res['leaderboard_id'])
            r = helpers.generic_delete(self.path, res['_id'])
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return r.content
