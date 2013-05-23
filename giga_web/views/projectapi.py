# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from helpers import generic_get, generic_delete
import json


class ProjectAPI(MethodView):

    def get(self, id, cid):
        if id is None:
            pass
        else:
            path = '/projects/'
            proj = generic_get(path, proj_id)
            return json.dumps(proj.content)

    def post(self, id=None, cid=None):
        if id is not None:
            pass  # patch
        else:
            client_id = request.form['client_id']
            camp_id = request.form['camp_id']
            name = request.form['name']
            perma_name = request.form['perma_name'].lower()
            descript = request.form['description']
            goal = request.form['goal']  # in cents
            typ = request.form['type']
            r = requests.get(crud_url + '/projects/',
                             params={'where': '{"perma_name":"' + perma_name + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    crypted = bcrypt.hashpw(pw, bcrypt.gensalt())
                    payload = {'data': {
                               'client_id': client_id,
                               'camp_id': camp_id,
                               'name': name,
                               'perma_name': perma_name,
                               'raised': 0,
                               'goal': goal,
                               'completed': False,
                               'descript': descript,
                               'type': typ}}
                    reg = requests.post(crud_url + '/projects/',
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'Project perma_name is not unique'})
            else:
                return json.dumps({'error': 'Cannot reach DB'})

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = generic_delete('/projects/', user_id)
            if r.status_code == requests.codes.ok:
                return json.dumps({'message': 'successful deletion'})
            else:
                return json.dumps(r.content)
