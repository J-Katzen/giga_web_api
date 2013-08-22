# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url, helpers
from giga_web.tasks import confirm_donation
from wsgiref.handlers import format_date_time
from datetime import datetime, timedelta
from time import mktime
import requests
import json

app = giga_web


@app.route("/confirm/<client_perma>/<campaign_perma>", methods=['POST'])
def confirm_client(client_perma, campaign_perma):
    if client_perma.lower() == 'moravian':
        cash_data = helpers.create_dict_from_form(request.form)
        res = confirm_moravian(client_perma, cash_data)
    else:
        res = {'error': 'could not get client'}
    return json.dumps(res)


def confirm_moravian(client_perma, cashnet_data):
    cl = helpers.generic_get('/clients/', client_perma)
    print cashnet_data
    cl_j = cl.json()
    client_id = cl_j['_id']
    email = cashnet_data['ref1val1']
    trans_id = cashnet_data['tx']
    client_trans_id = cashnet_data['ref2val1']
    #date = cashnet_data['effdate']
    total = int(float(cashnet_data['amount1'])) * 100
    #created before now, but after yesterday
    now = format_date_time(mktime(datetime.utcnow().timetuple()))
    yesterday = format_date_time(mktime((datetime.utcnow() - timedelta(days=1)).timetuple()))
    parm = {}
    parm = {'where': '{"email":"%s", "client_id": "%s", "total_donated": %d, "confirmed": {"$exists": false }, "created": {"$gte": "%s", "$lte": "%s"}}' %
            (email, client_id, total, yesterday, now)}
    r = requests.get(crud_url + '/donations/', params=parm)
    rj = r.json()
    if len(rj['_items']) > 0:
        donation = rj['_items'][0]
        donation['processor_trans_id'] = str(trans_id)
        donation['client_trans_id'] = str(client_trans_id)

        if 'result' in cashnet_data:
            res = cashnet_data['result']
        elif '&result' in cashnet_data:
            res = cashnet_data['&result']
        if res == 0:
            donation['confirmed'] = format_date_time(mktime(datetime.utcnow().timetuple()))
        else:
            donation['denied'] = format_date_time(mktime(datetime.utcnow().timetuple()))
        donation['confirm_source'] = 'cashnet'
        patched = helpers.generic_patch('/donations/', donation, donation['etag'])
        if 'confirmed' in donation:
            confirm_donation.delay(donation)
        return cashnet_data
    else:
        return {'error': 'bad transaction'}
