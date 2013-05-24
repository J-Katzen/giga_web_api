# -*- coding: utf-8 -*-

from giga_web import crud_url
from flask.views import MethodView
from flask import request
from helpers import generic_get, generic_delete, create_dict_from_form
import requests
import json
import bcrypt


class ClientAPI(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            path = '/clients/'
            client = generic_get(path, id)
            return json.dumps(client.content)

    def post(self, id=None):
        if id is not None:
            pass  # patch
        else:
            data = create_dict_from_form(request.form)
            r = requests.get(crud_url + '/clients/',
                             params={'where': '{"name":"' + name + '"}'})
            r2 = requests.get(crud_url + '/clients/' + perma_name)
            if (r.status_code == requests.codes.ok) and (r2.status_code == 404):
                res = r.json()
                if len(res['_items']) == 0:
                    payload = {'data': data}
                    reg = requests.post(crud_url + '/clients/',
                                        data=json.dumps(payload),
                                        headers={'Content-Type': 'application/json'})

                    return json.dumps(reg.content)
                else:
                    return json.dumps({'error': 'Client name is not unique'})
            elif r.status_code == r2.status_code == 404:
                return json.dumps({'error': 'Could not query DB'})
            elif r.status_code == r2.status_code == requests.codes.ok:
                res = r.json()
                if len(res['_items']) == 0:
                    return json.dumps({'error': 'perma_name not unique'})
                else:
                    return json.dumps({'error': 'name and perma_name not unique'})
            else:
                return json.dumps({'error': 'perma_name not unique'})

    def delete(self, id):
        if id is None:
            return json.dumps({'error': 'did not provide id'})
        else:
            r = requests.get(crud_url + '/clients/' + id)
            r_json = r.json()
            etag = r_json['etag']
            del_req = requests.delete(crud_url + '/clients/' + id,
                                      headers={'If-Match': etag})
