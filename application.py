# -*- coding: utf-8 -*-

from flask import Flask, request
import requests, bcrypt

application = Flask(__name__)
app = application
crud_url = 'http://giga-eve.elasticbeanstalk.com'

#login
@app.route("/login", methods=['POST'])
def login():
	email = str.lower(request.form['email'])
	pw = request.form['pw']
	r = requests.get(crud_url+'/users/'+email)
	if r.status_code == 200:
		res = r.json()
		if bcrypt.hashpw(pw,res['pw']) == res['pw']:
			return res
		else:
			return json.dumps({'error': 'Invalid password'})
	else:
		return json.dumps({'error': 'Could not query DB'})

#display user page
@app.route("/user/<email>")
def user(email):
	pass

@app.route("/<campaign_perma>")
def campaign(campaign_perma):
	return requests.get(crud_url+'/campaigns/'+campaign_perma)

@app.route("/<client_perma>")
def client(client_perma):
	return requests.get(crud_url+'/clients/'+client_perma)

@app.route("/<ObjectId:proj_id>")
def project(proj_id):
	return requests.get(crud_url+'/projects/'+proj_id)

@app.route("/<objectId:camp_id>/leaderboard")
def leaderboard(camp_perma):
	return requests.get(crud_url+'/leaderboards/?where={"camp_id":"'+camp_id+'"}')

@app.route("/create/<objectId:camp_id>/project")
def create_proj():
	pass

@app.route("/create/<objectId:camp_id>/leaderboard")
def create_lboard():
	pass

@app.route("/create/<objectId:camp_id>/donation")
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

	r = requests.get(crud_url+'/users/?where={"email":'+email+'}')
	if r.status_code == 200:
		res = r.json()
		if len(res['_items']) == 0:
			crypted = bcrypt.hashpw(pw,bcrypt.gensalt())
			payload = "item1={'email': email, 'pw': crypted, 'fb_login': False, 't_login': False }"
			reg = requests.post(crud_url+'/users/', data=payload)
			return reg
		else:
			return json.dumps({'error': 'User exists'})
	else:
		return json.dumps({'error': 'Could not query DB'})

if __name__ == '__main__':
    # Heroku support: bind to PORT if defined, otherwise default to 5000.
    port = 5001

    app.run(host='0.0.0.0', port=port)
