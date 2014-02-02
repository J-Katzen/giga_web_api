# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import User, UserStripeInfo, FBFriend
from giga_web.tasks import new_user_mail, verified_mail
from datetime import datetime
from flask.views import MethodView
from flask import request
import bcrypt


class UserAPI(MethodView):
    def get(self, id):
        if id is None:
            if 'email' in request.args:
                return User.objects.get_or_404(email=request.args['email']).select_related(2).to_json()
            elif 'facebook' in request.args:
                return User.objects.get_or_404(facebook_id=int(request.args['facebook'])).select_related(2).to_json()
            elif 'twitter' in request.args:
                return User.objects.get_or_404(twitter_id=int(request.args['twitter'])).select_related(2).to_json()
            # elif 'test' in request.args:
            #     users = User.objects
            #     return jsonify(result=users.to_json())
            else:
                return helpers.api_error('No user_id provided!', 404), 404
        else:
            return User.objects.get_or_404(id=id).select_related(2).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if 'email' in data:
            data['email'] = data['email'].lower()
            # verification email
        if 'password' in data:
            data['password'] = bcrypt.hashpw(
                data['password'], bcrypt.gensalt())
        if 'stripe_info' in data:
            data['stripe_info'] = UserStripeInfo(**data['stripe_info'])
        if 'fb_friends' in data:
            new_list = []
            for friend in data['fb_friends']:
                new_list.append(FBFriend(**friend))
            data['fb_friends'] = new_list
        if id is not None:
            user = User.objects.get_or_404(id=id)
            user = helpers.generic_update(user, data)
        else:
            user = User(**data)
            user.updated = datetime.utcnow()
            try:
                user.save()
            except ValidationError as e:
                return helpers.api_error(e.message, 400), 400
            except NotUniqueError as e:
                return helpers.api_error(e.message, 409), 409
            except Exception:
                return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        return helpers.api_return('OK', user.updated, user.id, 'User')

    def delete(self, id):
        if id is None:
            return helpers.api_error('No user_id provided!', 404), 404
        else:
            u = User.objects.get_or_404(id=id)
            u.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'User')
