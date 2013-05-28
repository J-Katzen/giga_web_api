# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import json
import requests


class ProjectAPI(MethodView):
    path = '/projects/'

    def get(self, cid, id):
        if id is None:
            parm = {'where': '{"client_id" : "%s"}' % cid}
            r = requests.get(crud_url + self.path,
                             params=parm)
            res = r.json()
            return json.dumps(res['_items'])
        else:
            proj = helpers.generic_get(self.path, proj_id)
            return proj.content

    def post(self, id=None):
        data = helpers.create_dict_from_form(request.form)
        if id is not None:
            pass  # patch & update
        else:
            data['raised'] = 0
            data['completed'] = False
            r = requests.get(crud_url + self.path,
                             params={'where': '{"perma_name":"' +
                                     data['perma_name'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type':
                                        'application/json'})
                    camp_append = self.campaign_append_proj(
                        json.loads(reg.content))
                    if json.loads(camp_append)['data']['status'] == 'OK':
                        return reg.content
                    else:
                        return json.dumps({'error': 'could not append proj'
                                           ' to campaign'})
                else:
                    return json.dumps({'error': 'Project perma_name is'
                                       ' not unique'})
            else:
                return json.dumps({'error': 'Cannot reach DB'})

    def campaign_update(self, proj_data):
        camp = helpers.generic_get('/campaigns/', proj_data['camp_id'])
        c = camp.json()
        proj = next((d for d in c['project_list'] if
                     d['p_id'] == proj_data['_id']), None)
        if proj is not None:
            for key, value in proj_data.iteritems():
                proj[key] = value

    def campaign_append_proj(self, proj_data):
        camp = helpers.generic_get('/campaigns/', proj_data['camp_id'])
        c = camp.json()
        c['project_list'].append({'p_id': proj_data['_id'],
                                  'proj_name': proj_data['name'],
                                  'votes': 0,
                                  'goal': proj_data['goal'],
                                  'description': proj_data['descript'][0:254]})
        c['total_goal'] += proj_data['goal']
        patched = helpers.generic_patch('/campaigns/', c)
        return patched.content

    def campaign_remove_proj(self, id):
        camp = helpers.generic_get(self.path, id)
        if camp.status_code == requests.codes.ok:
            cj = camp.json()
            c = helpers.generic_get('/campaigns/', cj['camp_id'])
            if c.status_code == requests.codes.ok:
                cam = c.json()
                proj = next((d for d in cam[
                            'project_list'] if d['p_id'] == id), None)
                cam['total_goal'] -= proj['goal']
                cam['project_list'].remove(proj)
                patched = helpers.generic_patch('/campaigns/', cam)
                return patched.json()
        else:
            return camp.json()

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            c = self.campaign_remove_proj(id)
            if c['data']['status'] == 'OK':
                r = helpers.generic_delete(self.path, id)
                if r.status_code == requests.codes.ok:
                    return json.dumps({'message': 'successful deletion'})
                else:
                    return r.content
            else:
                return json.dumps({'error': 'Could not remove proj from campaign'})
