# -*- coding: utf-8 -*-

from giga_web import giga_web
import requests
import bcrypt

app = giga_web


#login
@app.route("/login", methods=['POST'])
def login():
    email = str.lower(request.form['email'])
    pw = request.form['pw']
    r = requests.get(crud_url + '/users/' + email)
    if r.status_code == requests.codes.ok:
        res = r.json()
        if bcrypt.hashpw(pw, res['pw']) == res['pw']:
            return res
        else:
            return json.dumps({'error': 'Invalid password'})
    else:
        return json.dumps({'error': 'Could not query DB'})


# display user page
@app.route("/user/<objectid:id>")
def user(id):
    pass


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


@app.route("/register/user", methods=['POST'])
def register_user():
    email = str.lower(request.form['email'])
    pw = request.form['pw']

    r = requests.get(crud_url + '/users/?where={"email":' + email + '}')
    if r.status_code == requests.codes.ok:
        res = r.json()
        if len(res['_items']) == 0:
            crypted = bcrypt.hashpw(pw, bcrypt.gensalt())
            payload = {'data': {
                       'email': email,
                       'pw': crypted,
                       'fb_login': False,
                       't_login': False}}

            reg = requests.post(crud_url + '/users/',
                                data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'})
            return reg
        else:
            return json.dumps({'error': 'User exists'})
    else:
        return json.dumps({'error': 'Could not query DB'})
