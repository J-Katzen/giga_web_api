# -*- coding: utf-8 -*-

from flask import request
from giga_web import giga_web, crud_url
import helpers
import requests
import bcrypt
import json

app = giga_web


@app.route("/donation/confirm/", methods=['POST'])
def confirm_donation():
    #data = helpers.create_dict_from_form(request.form)
    pass
