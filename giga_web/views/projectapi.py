# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import Project, Organization, User, Reward, Post, MarketingList
from flask.views import MethodView
from flask import request, jsonify
from datetime import datetime

class ProjectAPI(MethodView):
    def get(self, id, cid=None, org_perma=None, proj_perma=None):
        if id is None:
            if cid is not None:
                # this is temporary - return list of projects for this cid?
                return helpers.api_error('No Project ID Provided!', 404), 404
            elif (org_perma is not None) and (proj_perma is not None):
                org = Organization.objects.get_or_404(perma_name=org_perma)
                return Project.objects.get_or_404(organization=org, perma_name=proj_perma).select_related(1).to_json()
            elif 'user' in request.args:
                u = User.objects.get_or_404(id=request.args['user'])
                projects = Project.objects(creator=u)
                return jsonify(result=projects.to_json())
            else:
                return helpers.api_error('No Project ID Provided!', 404), 404
        else:
            return Project.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if 'rewards' in data:
            reward_list = []
            for reward in data['rewards']:
                reward_list.append(Reward(**reward))
            data['rewards'] = reward_list
        if 'organization' in data:
            org = Organization.objects.get_or_404(id=data['organization'])
            data['organization'] = org
        if 'name' not in data:
            return helpers.api_error('Please enter an appropriate name for your project!', 400), 400
        user = User.objects.get_or_404(id=data['creator'])
        for key, value in data.iteritems():
            if key in ['start_date', 'end_date', 'fulfilled_date', 'published']:
                data[key] = datetime.strptime(value['date'], "%Y-%m-%d %H:%M:%S")
            else:
                data[key] = value
        data['creator'] = user
        proj = Project(**data)
        proj.updated = datetime.utcnow()
        try:
            proj.save()
        except ValidationError as e:
            return helpers.api_error(e.message, 400), 400
        except NotUniqueError as e:
            return helpers.api_error(e.message, 409), 409
        except Exception:
            return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        ml = MarketingList(project=proj.id, contacts=[], pledge_conversion=0, convert_conversion=0, total_donated=0)
        ml.save()
        return helpers.api_return("OK", proj.updated, proj.id, 'Project')

    def put(self, id):
        data = request.get_json(force=True, silent=False)
        if 'rewards' in data:
            reward_list = []
            for reward in data['rewards']:
                reward_list.append(Reward(**reward))
            data['rewards'] = reward_list
        if 'organization' in data:
            org = Organization.objects.get_or_404(id=data['organization'])
            data['organization'] = org
        proj = Project.objects.get_or_404(id=id)
        proj = helpers.generic_update(proj, data)
        # acceptable changes to name, twitter_hash, video_url, logo_url, 
        # description, rewards, tags, perma_name, 
        # pledge start date, start_date, end_date, 
        return helpers.api_return("OK", proj.updated, proj.id, 'Project')

    def delete(self, id):
        if id is None:
            return helpers.api_error('No Project ID Provided!', 404), 404
        else:
            p = Project.objects.get_or_404(id=id)
            p.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Project')
