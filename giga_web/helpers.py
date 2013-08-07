# -*- coding: utf-8 -*-

from flask import request
from giga_web import crud_url
import requests
import bcrypt
import json


def generic_get(collection_path, datum, projection=None):
    r = requests.get(crud_url + collection_path + datum + '/',
                     params=projection)
    if r.status_code == requests.codes.ok:
        return r
    else:
        err = {'error': 'Could not get from ' + collection_path}
        return err


def generic_patch(collection_path, data_dict, etag):
    new_data = dict()
    # don't try to patch eve keys or _id
    bad_keys = ['_links', 'created', 'etag', '_id', 'updated']
    r = requests.get(crud_url + collection_path + data_dict['_id'] + '/')
    if r.status_code == requests.codes.ok:
        obj_json = r.json()
        for key, value in data_dict.iteritems():
            # only specify fields that changed
            if key not in obj_json.keys():
                new_data[key] = value
            elif (obj_json[key] != value) and (key not in bad_keys):
                if value in ['True', 'true', 't']:
                    new_data[key] = True
                elif value in ['False', 'false', 'f']:
                    new_data[key] = False
                else:
                    new_data[key] = value
        dat = {'data': new_data}
        data_dict['_id'] = obj_json['_id']
        upd = requests.post(
            crud_url + collection_path + data_dict['_id'] + '/',
            data=json.dumps(dat),
            headers={'Content-Type': 'application/json',
                     'X-HTTP-Method-Override': 'PATCH',
                     'If-Match': etag})
        if upd.status_code == requests.codes.ok:
            return upd
        else:
            err = {'error': 'Could not correctly patch %s with the id of: %s' % (collection_path, data_dict['_id'])}
            return err
    else:
        err = {'error': 'Could not verify the data against the database'}
        return err


def get_index(seq, attr, value):
    idx = next((index for (index, d) in enumerate(seq) if d[attr] == value), None)
    return idx


def generic_delete(collection_path, id):
    r = requests.get(crud_url + collection_path + id + '/')
    if r.status_code == requests.codes.ok:
        res = r.json()
        d = requests.delete(crud_url + collection_path + id + '/',
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
        elif key in ['active', 'fb_login', 't_login', 'completed']:
            if value.lower() in ['true', 'yes', 't', '1']:
                d[key] = True
            else:
                d[key] = False
        elif value.isdigit():
            d[key] = int(value)
        else:
            d[key] = value
    return d
