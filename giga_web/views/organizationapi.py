# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from giga_web import helpers
from giga_web.models import Organization
from datetime import datetime
from flask.views import MethodView
from flask import request


class OrganizationAPI(MethodView):
    def get(self, id):
        if id is None:
            raise NotFound('No Organization ID Provided')
        else:
            return Organization.objects.get_or_404(id=id).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            org = Organization.objects.get_or_404(id=id)
            org = helpers.generic_update(org, data)
            org.updated = datetime.utcnow()
        else:
            org = Organization(**data)
            org.updated = datetime.utcnow()
        try:
            org.save()
        except ValidationError as e:
            raise BadRequest(e.errors)
        except NotUniqueError as e:
            raise BadRequest(e)
        except Exception:
            raise InternalServerError("Something went wrong! Check your request parameters!")
        return helpers.api_return('OK', org.updated, org.id, 'Organization')

    def delete(self, id):
        if id is None:
            raise NotFound('No Organization ID Provided!')
        else:
            o = Organization.objects.get_or_404(id=id)
            o.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Organization')
