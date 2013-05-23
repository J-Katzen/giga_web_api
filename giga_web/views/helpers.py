# -*- coding: utf-8 -*-

from flask import request
from giga_web import crud_url
import requests
import bcrypt


def generic_get(collection_path, datum, projection=None):
    r = requests.get(crud_url + collection_path + datum,
                     params=projection)
    if r.status_code == requests.codes.ok:
        return r
    else:
        err = {'error': 'Could not get from ' + collection_path}
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


def generic_patch(collection, id):
    for key, value in request.form.iteritems():
        print key, value
