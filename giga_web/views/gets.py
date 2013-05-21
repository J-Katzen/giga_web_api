# -*- coding: utf-8 -*-

from giga_web import giga_web, crud_url
import requests
import bcrypt
import json

app = giga_web


# display user page
@app.route("/users/<objectid:id>")
def user(id):
    pass


@app.route("/<campaign_perma>")
def campaign(campaign_perma):
    return requests.get(crud_url + '/campaigns/' + campaign_perma)


@app.route("/clients/<client_perma>")
def client(client_perma):
    return requests.get(crud_url + '/clients/' + client_perma)


@app.route("/projects/<objectid:proj_id>")
def project(proj_id):
    return requests.get(crud_url + '/projects/' + proj_id)


@app.route("/<objectid:camp_id>/leaderboard")
def leaderboard(camp_perma):
    return requests.get(crud_url + '/leaderboards/',
                        params={'where': '{"camp_id":"' + camp_id + '"}'})
