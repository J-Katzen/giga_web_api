# -*- coding: utf-8 -*-

from giga_web import giga_web, crud_url
import requests
import bcrypt
import json

app = giga_web


@app.route("/create/<objectid:camp_id>/project")
def create_proj(camp_id):
    pass


@app.route("/create/<objectid:camp_id>/leaderboard")
def create_lboard(camp_id):
    pass


@app.route("/create/<objectid:camp_id>/donation")
def create_donation(camp_id):
    pass


@app.route("/create/campaign")
def create_camp():
    pass
