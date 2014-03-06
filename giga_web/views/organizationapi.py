# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import Organization
from datetime import datetime
from flask.views import MethodView
from flask import request
from slugify import slugify


class OrganizationAPI(MethodView):
    def get(self, id):
        if id is None:
            return helpers.api_error('No Organization ID Provided', 404), 404
        else:
            return Organization.objects.get_or_404(id=id).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if 'name' not in data:
            raise helpers.api_error('Please enter an appropriate name for this Organization!', 400), 400
        elif 'perma_name' not in data:
            data['perma_name'] = slugify(data['name'])
        org = Organization(**data)
        org.updated = datetime.utcnow()
        try:
            org.save()
        except ValidationError as e:
            return helpers.api_error(e.message, 400), 400
        except NotUniqueError as e:
            return helpers.api_error(e.message, 409), 409
        except Exception:
            return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        return helpers.api_return('OK', org.updated, org.id, 'Organization')

    def put(self, id):
        data = request.get_json(force=True, silent=False)
        org = Organization.objects.get_or_404(id=id)
        org = helpers.generic_update(org, data)
        return helpers.api_return('OK', org.updated, org.id, 'Organization')


    def delete(self, id):
        if id is None:
            return helpers.api_error('No Organization ID Provided!', 404), 404
        else:
            o = Organization.objects.get_or_404(id=id)
            o.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Organization')
