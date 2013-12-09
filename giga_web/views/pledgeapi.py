# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from giga_web import helpers
from giga_web.models import Pledge
from datetime import datetime
from flask.views import MethodView
from flask import request

class PledgeAPI(MethodView):
    def get(self, id, cid=None):
        if id is None:
            raise NotFound('No Pledge ID Provided!')
        else:
            return Pledge.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            pledge = Pledge.objects.get_or_404(id=id)
            pledge = helpers.generic_update(pledge, data)
        else:
            pledge = Pledge(**data)
            pledge.updated = datetime.utcnow()
            try:
                pledge.save()
            except ValidationError as e:
                raise BadRequest(e.errors)
            except NotUniqueError as e:
                raise BadRequest(e)
            except Exception:
                raise InternalServerError("Something went wrong! Check your request parameters!")
        return helpers.api_return('OK', pledge.updated, pledge.id, 'Pledge')


    def delete(self, id):
        if id is None:
            raise NotFound('No Pledge ID Provided!')
        else:
            p = Pledge.objects.get_or_404(id=id)
            p.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Pledge')
