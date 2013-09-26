# -*- coding: utf-8 -*-

from giga_web import crud_url, helpers
from flask.views import MethodView
from flask import request
from datetime import datetime, timedelta
import json
import requests


class ProjectAPI(MethodView):
    path = '/projects/'

    def get(self, id, cid=None, camp_id=None, proj_perma=None):
        if id is None:
            if cid is not None:
                parm = {'where': '{"client_id" : "%s"}' % cid}
                r = requests.get(crud_url + self.path,
                                 params=parm)
                res = r.json()
                return json.dumps(res['_items'])
            elif (camp_id is not None) and (proj_perma is not None):
                parm = {'where': '{"camp_id": "%s", "perma_name": "%s"}'
                        % (camp_id, proj_perma)}
                r = requests.get(crud_url + self.path, params=parm)
                res = r.json()
                return json.dumps(res['_items'][0])

        else:
            proj = helpers.generic_get(self.path, id)
            return proj.content

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            data['_id'] = id
            proj = helpers.generic_get(self.path, id)
            proj_j = proj.json()

            # if goal or active state changes, update campaign active list
            if (proj_j['active'] != data['active']) or (proj_j['goal'] != data['goal']):
                c = self.campaign_remove_proj(id)
                if c['data']['status'] != 'OK':
                    patched = {'error': 'Could not update campaign properly'}
                    return json.dumps(patched)
                a = self.campaign_append_proj(data)
                if a['data']['status'] != 'OK':
                    patched = {'error': 'Could not append to campaign properly'}
                    return json.dumps(patched)
            # otherwise just patch project
            patched = helpers.generic_patch(self.path, data, data['etag'])
            if 'error' in patched:
                return json.dumps(patched)
            else:
                return patched.content
        else:
            data['raised'] = 0
            data['votes'] = 0
            r = requests.get(crud_url + self.path,
                             params={'where': '{"perma_name":"%s", "camp_id": "%s"}' % (data['perma_name'], data['camp_id'])})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + self.path,
                                        data=json.dumps(payload),
                                        headers={'Content-Type':
                                        'application/json'})
                    reg_j = reg.json()
                    print reg_j
                    if (reg_j['data']['status'] == 'OK'):
                        if data['active']:
                            data['_id'] = reg_j['data']['_id']
                            print data
                            camp_append = self.campaign_append_proj(data)
                            if 'error' not in camp_append:
                                if camp_append['data']['status'] == 'ERR':
                                    return camp_append['data']['issues']
                                return reg.content
                            else:
                                return json.dumps({'error': 'could not append proj'
                                                   ' to campaign'})
                        else:
                            return reg.content
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
        if 'summary' not in proj_data:
            summary = proj_data['description'][0:254]
            proj_data['summary'] = summary[:summary.rfind('.') + 1]
        else:
            proj_data['summary'] = proj_data['summary'][0:254]
            proj_data['summary'] = proj_data['summary'][:proj_data['summary'].rfind('.') + 1]
        app_proj = {'p_id': proj_data['_id'],
                    'proj_name': proj_data['name'],
                    'perma_name': proj_data['perma_name'],
                    'goal': proj_data['goal'],
                    'type': proj_data['type'],
                    'description': proj_data['summary'],
                    'raised': proj_data['raised']}
        if 'thumbnail' in proj_data:
            app_proj['proj_thumb'] = proj_data['thumbnail']
        if 'date_start' in c:
            app_proj['date_start'] = c['date_start']
        if proj_data['type'] != 'uncapped':
            c_start = datetime.strptime(c['date_start'], '%a, %d %b %Y %H:%M:%S GMT')
            d_end = (c_start + timedelta(proj_data['length'])).strftime('%a, %d %b %Y %H:%M:%S GMT')
            camp_end = datetime.strptime(c['date_end'], '%a, %d %b %Y %H:%M:%S GMT')
            dc_end = datetime.strptime(d_end, '%a, %d %b %Y %H:%M:%S GMT')
            if dc_end > camp_end:
                app_proj['date_end'] = c['date_end']
            else:
                app_proj['date_end'] = d_end
        else:
            app_proj['date_end'] = c['date_end']
        if proj_data['active'] and ('active_list' in c):
            c['active_list'].append(app_proj)
            c['total_goal'] += proj_data['goal']
        patched = helpers.generic_patch('/campaigns/', c, c['etag'])
        if 'error' in patched:
            return patched
        else:
            return patched.json()

    def campaign_remove_proj(self, id):
        proj = helpers.generic_get(self.path, id)
        if proj.status_code == requests.codes.ok:
            cj = proj.json()
            c = helpers.generic_get('/campaigns/', cj['camp_id'])
            if c.status_code == requests.codes.ok:
                cam = c.json()
                cur_len = len(cam['active_list'])
                cam['active_list'][:] = [d for d in cam['active_list']
                                         if d['p_id'] != cj['_id']]
                if cur_len != len(cam['active_list']):
                    cam['total_goal'] -= cj['goal']
                patched = helpers.generic_patch('/campaigns/', cam, cam['etag'])
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
