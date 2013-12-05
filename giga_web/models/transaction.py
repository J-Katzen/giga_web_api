# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization
from .user import User
from .project import Project


class Transaction(db.Document):
    organization = db.ReferenceField(Organization)
    project = db.ReferenceField(Project)
    user = db.ReferenceField(User)
    referring_user = db.ReferenceField(User)
    giga_fee = db.IntField(required=True)
    trans_fee = db.IntField(required=True)
    net_amt = db.IntField(required=True)
    total_amt = db.IntField(required=True)
    comment = db.StringField()
    updated = db.DateTimeField()
    meta = {
    	'indexes': ['organization', 'user', 'project', 'referring_user']
    }
