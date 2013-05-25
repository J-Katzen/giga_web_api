# -*- coding: utf-8 -*-

from flask.views import MethodView
from projectapi import ProjectAPI
from leaderboardapi import LeaderboardAPI
from flask import request
import json
import helpers


class CampaignAPI(MethodView):

    def get(self, campaign_perma):
        if campaign_perma is None:
            pass
        else:
            path = '/campaigns/'
            camp = helpers.generic_get(path, campaign_perma)
            return json.dumps(camp.content)

    def post(self, campaign_perma=None):
        if campaign_perma is not None:
            pass
        else:
            #needs name, perma_name, client_id, date_start, date_end, 
            data = helpers.create_dict_from_form(request.form)
            data['total_raised'] = 0
            r = requests.get(crud_url + '/campaigns/',
                             params={'where': '{"perma_name":"' + data['perma_name'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + '/campaigns/',
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'Campaign_perma exists'})
            else:
                return json.dumps({'error': 'Could not query DB'})

    def delete(self, campaign_perma):
        if campaign_perma is None:
            return json.dumps({'error': 'did not provide campaign_perma'})
        else:
            camp = helpers.generic_get(path, campaign_perma)
            res = camp.json()
            for proj in res['project_list']:
                d = helpers.generic_delete('/projects/', proj['p_id'])
            r = helpers.generic_delete('/campaigns/', user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
