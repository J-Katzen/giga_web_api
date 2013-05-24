# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
from helpers import generic_get, generic_delete, create_dict_from_form
import json
import requests


class ProjectAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/projects/'
            proj = generic_get(path, proj_id)
            return json.dumps(proj.content)

    def post(self, id=None):
        if id is not None:
            pass  # patch
        else:
            data = create_dict_from_form(request.form)
            data['raised'] = 0
            data['completed'] = False
            r = requests.get(crud_url + '/projects/',
                             params={'where': '{"perma_name":"' + data['perma_name'] + '"}'})
            if r.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
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
