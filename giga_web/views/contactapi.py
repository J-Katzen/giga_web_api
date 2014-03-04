# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import MarketingList, Contact
from datetime import datetime
from flask.views import MethodView
from flask import request

class ContactAPI(MethodView):
    def get(self, ml_id, email=None):
        email = request.args.get('email', None)
        if ml_id is None or email is None:
            return helpers.api_error('No Contact ID Provided!', 404), 404
        else:
            return MarketingList.objects.get_or_404(id=ml_id, contacts__email=email).select_related(1).to_json()

    def post(self, ml_id, email=None):
        email = request.args.get('email', None)
        data = request.get_json(force=True, silent=False)
        contact = Contact(**data)
        ml = 0
        if email is not None:
            ml = MarketingList.objects(id=ml_id, contacts__email=email).update(set__contacts__S=contact)
        if ml == 0:
            ml = MarketingList.objects(id=ml_id).update(push__contacts=contact)
        return helpers.api_return('OK', datetime.utcnow(), ml_id, 'Contact')

    def delete(self, ml_id, email=None):
        email = request.args.get('email', None)
        if ml_id is None or email is None:
            return helpers.api_error('No Contact ID Provided!', 404), 404
        else:
            ml = MarketingList.objects(id=ml_id).update(pull__contacts__email=email)
            return helpers.api_return('DELETED', datetime.utcnow(), ml_id, 'Contact')
