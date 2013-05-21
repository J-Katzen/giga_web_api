# -*- coding: utf-8 -*-

from giga_web import giga_web, crud_url
import requests
import bcrypt
import json

app = giga_web


# display user page
@app.route("/user/<objectid:id>")
def user(id):
    pass


#make a generic function that takes projections
@app.route("/<campaign_perma>")
def campaign(campaign_perma):
    return requests.get(crud_url + '/campaigns/' + campaign_perma)


@app.route("/<client_perma>")
def client(client_perma):
    return requests.get(crud_url + '/clients/' + client_perma)


@app.route("/<objectid:proj_id>")
def project(proj_id):
    return requests.get(crud_url + '/projects/' + proj_id)


@app.route("/<objectid:camp_id>/leaderboard")
def leaderboard(camp_perma):
    return requests.get(crud_url + '/leaderboards/',
                        params={'where': '{"camp_id":"' + camp_id + '"}'})


@app.route("/create/<objectid:camp_id>/project")
def create_proj():
    pass


@app.route("/create/<objectid:camp_id>/leaderboard")
def create_lboard():
    pass


@app.route("/create/<objectid:camp_id>/donation")
def create_donation():
    pass


@app.route("/create/campaign")
def create_camp():
    pass


@app.route("/register/client")
def register_user():
    pass
