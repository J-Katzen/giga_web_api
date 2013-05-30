# -*- coding: utf-8 -*-

from flask import request
from giga_web import crud_url
import requests
import bcrypt
import json


def generic_get(collection_path, datum, projection=None):
    r = requests.get(crud_url + collection_path + datum,
                     params=projection)
    if r.status_code == requests.codes.ok:
        return r
    else:
        err = {'error': 'Could not get from ' + collection_path}
        return err


def generic_patch(collection_path, data_dict):
    new_data = dict()
    r = requests.get(crud_url + collection_path + data_dict['_id'])
    if r.status_code == requests.codes.ok:
        obj_json = r.json()
        for key, value in data_dict.iteritems():
            if obj_json[key] != value: #only specify fields that changed
                new_data[key] = value
        dat = {'data': new_data}
        upd = requests.post(crud_url + collection_path + data_dict['_id']+'/',
                            data=json.dumps(dat),
                            headers={'Content-Type': 'application/json',
                                     'X-HTTP-Method-Override': 'PATCH',
                                     'If-Match': obj_json['etag']})
        if upd.status_code == requests.codes.ok:
            return upd
        else:
            err = {'error': 'Could not correctly patch '
                   + collection_path + ' with the id of: ' + data_dict['_id']}
            return err


def generic_delete(collection_path, id):
    r = requests.get(crud_url + collection_path + id)
    if r.status_code == requests.codes.ok:
        res = r.json()
        d = requests.delete(crud_url + collection_path + id,
                            headers={'If-Match': res['etag']})
        return d
    else:
        err = {'error': 'Could not find element in' +
               collection_path + ' with id ' + id}
        return err


def create_dict_from_form(req_form):
    d = {}
    for key, value in req_form.iteritems():
        if key in ['email', 'uname', 'perma_name']:
            d[key] = value.lower()
        elif key in ['active', 'fb_login', 't_login']:
            if value.lower() in ['true', 'yes', 't', '1']:
                d[key] = True
            else:
                d[key] = False
        elif value.isdigit():
            d[key] = int(value)
        else:
            d[key] = value
    return d
