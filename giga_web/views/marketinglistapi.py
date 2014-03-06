# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import MarketingList, Contact
from datetime import datetime
from flask.views import MethodView
from flask import request

class MarketingListAPI(MethodView):
    def get(self, id):
        if id is None:
            return helpers.api_error('No MarketingList ID Provided!', 404), 404
        else:
            return MarketingList.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        ml = MarketingList(**data)
        ml.updated = datetime.utcnow()
        try:
            ml.save()
        except ValidationError as e:
            return helpers.api_error(e.message, 400), 400
        except NotUniqueError as e:
            return helpers.api_error(e.message, 409), 409
        except Exception:
            return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        return helpers.api_return('OK', ml.updated, ml.id, 'MarketingList')

    def put(self, id):
        data = request.get_json(force=True, silent=False)
        ml = MarketingList.objects.get_or_404(id=id)
        ml = helpers.generic_update(ml, data)
        return helpers.api_return('OK', ml.updated, ml.id, 'MarketingList')

    def delete(self, id):
        if id is None:
            return helpers.api_error('No MarketingList ID Provided!', 404), 404
        else:
            p = MarketingList.objects.get_or_404(id=id)
            p.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'MarketingList')
