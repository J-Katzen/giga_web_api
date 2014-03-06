# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import Pledge
from datetime import datetime
from flask.views import MethodView
from flask import request

class PledgeAPI(MethodView):
    def get(self, id):
        if id is None:
            return helpers.api_error('No Pledge ID Provided!', 404), 404
        else:
            return Pledge.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        pledge = Pledge(**data)
        pledge.updated = datetime.utcnow()
        try:
            pledge.save()
        except ValidationError as e:
            return helpers.api_error(e.message, 400), 400
        except NotUniqueError as e:
            return helpers.api_error(e.message, 409), 409
        except Exception:
            return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        return helpers.api_return('OK', pledge.updated, pledge.id, 'Pledge')

    def put(self, id):
        data = request.get_json(force=True, silent=False)
        pledge = Pledge.objects.get_or_404(id=id)
        pledge = helpers.generic_update(pledge, data)
        return helpers.api_return('OK', pledge.updated, pledge.id, 'Pledge')

    def delete(self, id):
        if id is None:
            return helpers.api_error('No Pledge ID Provided!', 404), 404
        else:
            p = Pledge.objects.get_or_404(id=id)
            p.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Pledge')
