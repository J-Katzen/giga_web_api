# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
import helpers
import json
import requests


class ProjectAPI(MethodView):
    path = '/projects/'

    def get(self, id, cid=None):
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
            data['_id'] = id
            proj = helpers.generic_get(self.path, id)
            proj_j = proj.json()

            # if goal or active state changes, update campaign active list
            if (proj_j['active'] != data['active']) or proj_j['goal'] != data['goal']:
                c = self.campaign_remove_proj(id)
                if c['data']['status'] != 'OK':
                    patched = {'error': 'Could not update campaign properly'}
                    return patched
                a = self.campaign_append_proj(data)
                if json.loads(a)['data']['status'] != 'OK':
                    patched = {'error': 'Could not append to campaign properly'}
                    return patched

            # otherwise just patch project
            patched = helpers.generic_patch(self.path, data)
            if 'error' in patched:
                return patched
            else:
                return patched.content
        else:
            data['raised'] = 0
            if data['type'] == 'rolling':
                data['completed'] = False
            data['votes'] = 0
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
                    reg_j = reg.json()
                    if (reg_j['data']['status'] == 'OK') and (data['active'] in ['True', 'true', 't', 1]):
                        data['_id'] = reg_j['_id']
                        camp_append = self.campaign_append_proj(data)
                        if json.loads(camp_append)['data']['status'] == 'OK':
                            return reg.content
                        else:
                            return json.dumps({'error': 'could not append proj'
                                               ' to campaign'})
                    else:
                        return json.dumps({'error': 'Could not post project'})
                else:
                    return json.dumps({'error': 'Project perma_name is'
                                       ' not unique'})
            else:
                return json.dumps({'error': 'Cannot reach DB'})

    def campaign_append_proj(self, proj_data):
        camp = helpers.generic_get('/campaigns/', proj_data['camp_id'])
        c = camp.json()
        if proj_data['active']:
            c['active_list'].append({'p_id': proj_data['_id'],
                                     'proj_name': proj_data['name'],
                                     'perma_name': proj_data['perma_name'],
                                     'goal': proj_data['goal'],
                                     'description': proj_data['description'][0:254],
                                     'type': proj_data['type'],
                                     'date_start': c['date_start']})
        c['total_goal'] += proj_data['goal']
        patched = helpers.generic_patch('/campaigns/', c)
        return patched.content

    def campaign_remove_proj(self, id):
        proj = helpers.generic_get(self.path, id)
        if proj.status_code == requests.codes.ok:
            cj = proj.json()
            c = helpers.generic_get('/campaigns/', cj['camp_id'])
            if c.status_code == requests.codes.ok:
                cam = c.json()
                cam['total_goal'] -= proj['goal']
                cam['active_list'][:] = [d for d in cam['active_list']
                                         if d['_id'] != cj['_id']]
                patched = helpers.generic_patch('/campaigns/', cam)
                return patched.json()
        else:
            return proj.json()

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
