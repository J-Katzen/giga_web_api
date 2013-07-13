# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url
from giga_web.views import DonationAPI
import helpers
import requests
import json

app = giga_web


@app.route("/<client_perma>/donation/confirm/", methods=['POST'])
def confirm_donation(client_perma):
    if client_perma.lower() == 'moravian':
        cash_data = helpers.create_dict_from_form(request.form)
        res = confirm_moravian(client_perma, cash_data)
    return res


def confirm_moravian(client_perma, cashnet_data):
    pass
