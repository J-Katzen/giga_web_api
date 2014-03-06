# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import MarketingList, Contact
from datetime import datetime
from flask.views import MethodView
from flask import request
from bson.objectid import ObjectId

class ContactAPI(MethodView):
    def get(self, ml_id, id=None):
        email = request.args.get('email', None)
        if ml_id is not None:
            if id is not None:
                return MarketingList.objects.get_or_404(id=ml_id, contacts__con_id=id).to_json()
            if email is not None:
                return MarketingList.objects.get_or_404(id=ml_id, contacts__email=email).to_json()
        return helpers.api_error('No Contact ID Provided!', 404), 404

    def post(self, ml_id, id=None):
        data = request.get_json(force=True, silent=False)
        data['con_id'] = ObjectId()
        contact = Contact(**data)
        ml = 0
        if email is not None:
            ml = MarketingList.objects(id=ml_id, contacts__email=email).update(set__contacts__S=contact)
        if ml == 0:
            ml = MarketingList.objects(id=ml_id).update(push__contacts=contact)
        return helpers.api_return('OK', datetime.utcnow(), ml_id, 'Contact')

    def put(self, ml_id, id):
        data = request.get_json(force=True, silent=False)
        contact = Contact(**data)
        ml = MarketingList.objects(id=ml_id, contacts__con_id=id).update(set__contacts__S=contact)
        return helpers.api_return('OK', datetime.utcnow(), ml_id, 'Contact')

    def delete(self, ml_id, id):
        email = request.args.get('email', None)
        if ml_id is None or email is None:
            return helpers.api_error('No Contact ID Provided!', 404), 404
        else:
            ml = MarketingList.objects(id=ml_id).update(pull__contacts__email=email)
            return helpers.api_return('DELETED', datetime.utcnow(), ml_id, 'Contact')
