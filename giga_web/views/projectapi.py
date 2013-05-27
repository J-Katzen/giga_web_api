# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import json
import requests


class ProjectAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/projects/'
            proj = helpers.generic_get(path, proj_id)
            return json.dumps(proj.content)

    def post(self, id=None):
        if id is not None:
            pass  # patch
        else:
            data = helpers.create_dict_from_form(request.form)
            data['raised'] = 0
            data['completed'] = False
            r = requests.get(crud_url + '/projects/',
                             params={'where': '{"perma_name":"' +
                                     data['perma_name'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + '/projects/',
                                        data=json.dumps(payload),
                                        headers={'Content-Type':
                                        'application/json'})
                    camp_append = self.campaign_append_proj(
                        json.loads(reg.content))
                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'Project perma_name is'
                                       ' not unique'})
            else:
                return json.dumps({'error': 'Cannot reach DB'})

    def campaign_append_proj(self, proj_data):
        camp = helpers.generic_get('/campaigns/', proj_data['camp_id'])
        c = camp.json()
        c['project_list'].append({'p_id': proj_data['_id'],
                                  'proj_name': proj_data['name'],
                                  'votes': 0,
                                  'goal': proj_data['goal'],
                                  'description': proj_data['descript'][0:254]})
        patched = helpers.generic_patch('/campaigns/', c)
        return json.dumps(patched.content)

    def campaign_remove_proj(self, id):
        camp = helpers.generic_get('/projects/', id)
        if camp.status_code == requests.codes.ok:
            cj = camp.json()
            c = helpers.generic_get('/campaigns/' cj['camp_id'])
            if c.status_code == requests.codes.ok:
                cam = c.json()
                cam['project_list'][:] = [d for d in cam['project_list'] if d.get('p_id') != id]
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
                r = helpers.generic_delete('/projects/', id)
                if r.status_code == requests.codes.ok:
                    return json.dumps({'message': 'successful deletion'})
                else:
                    return json.dumps(r.content)
            else:
                return json.dumps({'error': 'Could not remove proj'
                                   ' from campaign'})
