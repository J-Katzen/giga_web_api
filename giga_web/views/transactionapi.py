# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from giga_web import helpers
from giga_web.models import Transaction, Project, User, Organization, MarketingList
from giga_web.tasks import thank_you_mail
from datetime import datetime
from flask.views import MethodView
from flask import request, jsonify


class TransactionAPI(MethodView):
    def get(self, id, cid=None):
        if id is None:
            if cid is not None:
                return helpers.api_error('No Transaction ID Provided!', 404), 404
            elif 'project' in request.args:
                p = Project.objects.get_or_404(id=request.args['project'])
                trans = Transaction.objects(project=p).order_by('-created')
                return jsonify(result=trans.to_json())
        else:
            return Transaction.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        proj = Project.objects.get_or_404(id=data['project'])
        transaction = Transaction(fullname=data['fullname'], email=data['email'], project=proj, total_amt=data['total_amt'],
            giga_fee=data['giga_fee'], trans_fee=data['trans_fee'], net_amt=data['net_amt'],
            stripe_id=data['stripe_id'], survey_fields=data['survey_fields'])
        if 'comment' in data:
            transaction.comment = data['comment']
        if 'referring_user' in data:
            ref = User.objects.get_or_404(id=data['referring_user'])
            transaction.referring_user = ref
        if 'organization' in data:
            org = Organization.objects.get_or_404(id=data['organization'])
            transaction.organization=org
        if 'user' in data:
            user = User.objects.get_or_404(id=data['user'])
            transaction.user=user
        transaction.updated = datetime.utcnow()
        transaction.created = datetime.utcnow()
        try:
            transaction.save()
        except ValidationError as e:
            return helpers.api_error(e.message, 400), 400
        except NotUniqueError as e:
            return helpers.api_error(e.message, 409), 409
        except Exception:
            return helpers.api_error("Something went wrong! Check your request parameters!", 500), 500
        proj.update(inc__total_raised=data['total_amt'],
                    inc__total_giga_fee=data['giga_fee'],
                    inc__total_trans_fee=data['trans_fee'],
                    inc__total_net_raised=data['net_amt'],
                    add_to_set__donor_list=data['email'])
        ml = MarketingList.objects(project=proj.id, contacts__email=data['email']).update(set__contacts__S__status='converted', 
                                                                                          set__contacts__S__donated=data['total_amt'])
        if ml > 0:
            ml = MarketingList.objects(project=proj.id).update(inc__convert_conversion=1,
                                                               inc__total_donated=data['total_amt'])
        return helpers.api_return('OK', transaction.updated, transaction.id, 'Transaction')

    def put(self, id):
        data = request.get_json(force=True, silent=False)
        transaction = Transaction.objects.get_or_404(id=id)
        if 'total_amt' in data:
            org = transaction.organization
            diff = data['total_amt'] - transaction.total_amt
            if org is not None:
                diff_giga = ((data['total_amt']*(org.giga_fee_percent/10000.0))+org.giga_fee_cents)-transaction.giga_fee
                diff_trans = ((data['total_amt']*(org.trans_fee_percent/10000.0))+org.trans_fee_cents)-transaction.trans_fee
                net_amt = (data['total_amt']-(diff_giga+diff_trans))-transaction.net_amt
            else:
                diff_giga = (data['total_amt']*0.05)-transaction.giga_fee
                diff_trans = ((data['total_amt']*0.029)+30)-transaction.trans_fee
                net_amt = (data['total_amt']-(diff_giga+diff_trans))-transaction.net_amt
            Project.objects(id=transaction.project.id).update_one(inc__total_raised=diff,
                                                                  inc__total_giga_fee=diff_giga,
                                                                  inc__total_trans_fee=diff_trans,
                                                                  inc__total_net_raised=net_amt)
        if 'comment' in data:
            transaction.comment = data['comment']
        if 'referring_user' in data:
            ref = User.objects.get_or_404(id=data['referring_user'])
            transaction.referring_user = ref
        if 'organization' in data:
            org = Organization.objects.get_or_404(id=data['organization'])
            transaction.organization=org
        if 'user' in data:
            user = User.objects.get_or_404(id=data['user'])
            transaction.user=user
        transaction = helpers.generic_update(transaction, data)
        return helpers.api_return('OK', transaction.updated, transaction.id, 'Transaction')


    def delete(self, id):
        if id is None:
            return helpers.api_error('No Transaction ID Provided!', 404), 404
        else:
            t = Transaction.objects.get_or_404(id=id)
            Project.objects(id=t.project.id).update_one(dec__total_raised=t.total_amt,
                                                        dec__total_giga_fee=t.giga_fee,
                                                        dec__total_trans_fee=t.trans_fee,
                                                        dec__total_net_raised=t.net_amt,
                                                        pull__donor_list=t.email)
            t.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Transaction')
