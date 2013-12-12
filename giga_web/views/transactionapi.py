# -*- coding: utf-8 -*-
from mongoengine.errors import ValidationError, NotUniqueError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
from giga_web import helpers
from giga_web.models import Transaction, Project, User, Organization
from datetime import datetime
from flask.views import MethodView
from flask import request


class TransactionAPI(MethodView):
    def get(self, id, cid=None):
        if id is None:
            raise NotFound('No Transaction ID Provided!')
        else:
            return Transaction.objects.get_or_404(id=id).select_related(1).to_json()

    def post(self, id=None):
        data = request.get_json(force=True, silent=False)
        if id is not None:
            transaction = Transaction.objects.get_or_404(id=id)
            if 'total_amt' in data:
                org = transaction.organization
                diff = data['total_amt'] - transaction.total_amt
                diff_giga = ((data['total_amt']*(org.giga_fee_percent/10000.0))+org.giga_fee_cents)-transaction.giga_fee
                diff_trans = ((data['total_amt']*(org.trans_fee_percent/10000.0))+org.trans_fee_cents)-transaction.trans_fee
                net_amt = (data['total_amt']-(diff_giga+diff_trans))-transaction.net_amt
                Project.objects(id=transaction.project.id).update_one(inc__total_raised=diff,
                                                                      inc__total_giga_fee=diff_giga,
                                                                      inc__total_trans_fee=diff_trans,
                                                                      inc__total_net_raised=net_amt)
            transaction = helpers.generic_update(transaction, data)
        else:
            proj = Project.objects.get_or_404(id=data['project'])
            user = User.objects.get_or_404(id=data['user'])
            org = Organization.objects.get_or_404(id=data['organization'])
            transaction = Transaction(organization=org, project=proj, user=user, total_amt=data['total_amt'],
                giga_fee=data['giga_fee'], trans_fee=data['trans_fee'], net_amt=data['net_amt'])
            if 'comment' in data:
                transaction.comment = data['comment']
            if 'referring_user' in data:
                ref = User.objects.get_or_404(id=data['referring_user'])
                transaction.referring_user = ref
            transaction.updated = datetime.utcnow()
            try:
                transaction.save()
            except ValidationError as e:
                raise BadRequest(e.errors)
            except NotUniqueError as e:
                raise BadRequest(e)
            except Exception:
                raise InternalServerError("Something went wrong! Check your request parameters!")
            proj.update(inc__total_raised=data['total_amt'],
                        inc__total_giga_fee=data['giga_fee'],
                        inc__total_trans_fee=data['trans_fee'],
                        inc__total_net_raised=data['net_amt'],
                        add_to_set__donor_list=user)
        return helpers.api_return('OK', transaction.updated, transaction.id, 'Transaction')

    def delete(self, id):
        if id is None:
            raise NotFound('No Transaction ID Provided!')
        else:
            t = Transaction.objects.get_or_404(id=id)
            u = User.objects.get_or_404(id=t.user.id)
            Project.objects(id=t.project.id).update_one(dec__total_raised=t.total_amt,
                                                        dec__total_giga_fee=t.giga_fee,
                                                        dec__total_trans_fee=t.trans_fee,
                                                        dec__total_net_amt=t.net_amt,
                                                        pull__donor_list=u)
            t.delete()
            return helpers.api_return('DELETED', datetime.utcnow(), id, 'Transaction')