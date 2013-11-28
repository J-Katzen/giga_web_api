# -*- coding: utf-8 -*-
from giga_web import giga_web
import requests
import json

app = giga_web


@app.route("/user/<uid>/transactions/", methods=['GET'])
def user_transactions(uid):
    parm = {'where': '{"user_id": "%s"}' % uid}
    r = requests.get(crud_url + '/donations/', params=parm)
    res = r.json()
    if len(res['_items']) > 0:
        return json.dumps(res['_items'])
    else:
        return json.dumps({'error': 'No items'})
