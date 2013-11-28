# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from giga_web import helpers
from giga_web.models import User
from giga_web.tasks import new_user_mail, verified_mail
from datetime import datetime
from flask.views import MethodView
from flask import request
import json
import bcrypt


class UserAPI(MethodView):

    def get(self, id):
        if id is None:
            raise NotFound('No user_id provided!')
        else:
            return User.objects.get_or_404(id=id).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if 'email' in data:
            data['email'] = data['email'].lower()
        if 'password' in data:
            data['password'] = bcrypt.hashpw(
                data['password'], bcrypt.gensalt())
        if id is not None:
            o_user = User.objects.get_or_404(id=id)
            o_user = helpers.generic_update(o_user, data)
            o_user.updated = datetime.utcnow()
            try:
                o_user.save()
            except ValidationError as e:
                raise BadRequest(json.dumps(e.errors))
            except NotUniqueError as e:
                raise BadRequest(e)
            except Exception:
                raise InternalServerError("Something went wrong! Check your parameters!")
            return helpers.api_return('OK', o_user.updated, o_user.id, 'User')
        else:
            n_user = User(**data)
            n_user.updated = datetime.utcnow()
            try:
                n_user.save()
            except ValidationError as e:
                raise BadRequest(e.errors)
            except NotUniqueError as e:
                raise BadRequest(e)
            except Exception:
                raise InternalServerError("Something went wrong! Check your parameters!")
            return helpers.api_return('OK', n_user.updated, n_user.id, 'User')

    def delete(self, id):
        if id is None:
            raise NotFound('No user_id provided!')
        else:
            u = User.objects.get_or_404(id=id)
            u.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'User')
