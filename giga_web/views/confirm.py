# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url, helpers
from giga_web.views import DonationAPI
import requests
import json

app = giga_web


@app.route("/confirm/<client_perma>/<campaign_perma>", methods=['POST'])
def confirm_donation(client_perma, campaign_perma):
    if client_perma.lower() == 'moravian':
        cash_data = helpers.create_dict_from_form(request.form)
        res = confirm_moravian(client_perma, cash_data)
    else:
        res = {'error': 'could not get client'}
    return json.dumps(res)


def confirm_moravian(client_perma, cashnet_data):
    print cashnet_data
    if cashnet_data['result'] == 0:
        client = helpers.generic_get('/clients/', client_perma)
        client_json = client.json()
        print cashnet_data
        return cashnet_data
    else:
        return {'error': 'bad transaction'}
