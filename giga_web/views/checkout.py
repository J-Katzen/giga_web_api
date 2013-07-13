# -*- coding: utf-8 -*-

from giga_web import giga_web, crud_url
import requests
import json

app = giga_web


@app.route("/checkout/<camp_perma>/", methods=['GET'])
def checkout_project(camp_perma):
    parm = {'where': '{"type": "checkout"}'}
    r = requests.get(crud_url + '/projects/', params=parm)
    res = r.json()
    if len(res['_items']) > 0:
        return json.dumps(res['_items'][0])
    else:
        return json.dumps({'error': 'There are no checkout projects'})
