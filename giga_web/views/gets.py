# -*- coding: utf-8 -*-

from giga_web import giga_web, crud_url
import requests
import bcrypt
import json

app = giga_web


def generic_get(collection_path, datum, projection=None):
    r = requests.get(crud_url + collection_path + datum,
                     params=projection)
    if r.status_code == requests.codes.ok:
        return r
    else:
        return json.dumps({'error': 'Could not get from ' + collection_path})
# display user page


@app.route("/users/<id>")
def user(id):
    path = '/users/'
    g = generic_get(path, id)
    return json.dumps(g.content)


@app.route("/campaigns/<campaign_perma>")
def campaign(campaign_perma):
    path = '/campaign/'
    g = generic_get(path, campaign_perma)
    return json.dumps(g.content)


@app.route("/clients/<client_perma>")
def client(client_perma):
    path = '/clients/'
    g = generic_get(path, client_perma)
    return json.dumps(g.content)


@app.route("/projects/<proj_id>")
def project(proj_id):
    path = '/projects/'
    g = generic_get(path, proj_id)
    return json.dumps(g.content)


@app.route("/<objectid:camp_id>/leaderboard")
def leaderboard(camp_perma):
    return requests.get(crud_url + '/leaderboards/',
                        params={'where': '{"camp_id":"' + camp_id + '"}'})
