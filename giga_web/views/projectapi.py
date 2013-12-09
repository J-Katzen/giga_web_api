# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from giga_web import helpers
from giga_web.models import Project, Organization, User
from flask.views import MethodView
from flask import request
from datetime import datetime
from slugify import slugify

class ProjectAPI(MethodView):
    def get(self, id, cid=None, org_id=None, proj_perma=None):
        if id is None:
            if cid is not None:
                pass
            elif (org_id is not None) and (proj_perma is not None):
                org = Organization.objects.get_or_404(id=org_id)
                return Project.objects.get_or_404(organization=org, perma_name=proj_perma).select_related(1).to_json()
            else:
                raise NotFound('No Project ID Provided!')
        else:
            return Project.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if 'name' not in data:
            raise BadRequest('Please enter an appropriate name for your project!')
        elif 'perma_name' not in data:
            data['perma_name'] = slugify(data['name'])
        if id is not None:
            proj = Project.objects.get_or_404(id=id)
            proj = helpers.generic_update(proj, data)
            # acceptable changes to name, twitter_hash, video_url, logo_url, 
            # description, rewards, tags, perma_name, 
            # pledge start date, start_date, end_date, 
        else:
            user = User.objects.get_or_404(id=data['user'])
            org = Organization.objects.get_or_404(id=data['organization'])
            data['user'] = user
            data['organization'] = org
            proj = Project(**data)
            proj.updated = datetime.utcnow()
            try:
                proj.save()
            except ValidationError as e:
                raise BadRequest(e.errors)
            except NotUniqueError as e:
                raise BadRequest(e)
            except Exception:
                raise InternalServerError("Something went wrong! Check your request parameters!")
        return helpers.api_return("OK", proj.updated, proj.id, 'Project')

    def delete(self, id):
        if id is None:
            raise NotFound('No Project ID Provided!')
        else:
            p = Project.objects.get_or_404(id=id)
            p.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Project')