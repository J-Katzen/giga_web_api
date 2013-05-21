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
        return json.dumps({'error': 'Could not get from ' + collection_path})