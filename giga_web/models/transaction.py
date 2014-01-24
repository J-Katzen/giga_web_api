# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization
from .user import User
from .project import Project


class Transaction(db.Document):
    organization = db.ReferenceField(Organization)
    project = db.ReferenceField(Project)
    email = db.EmailField(required=True)
    user = db.ReferenceField(User)
    referring_user = db.ReferenceField(User)
    stripe_id = db.StringField(required=True, unique=True)
    status = db.StringField()
    giga_fee = db.IntField(required=True)
    trans_fee = db.IntField(required=True)
    net_amt = db.IntField(required=True)
    total_amt = db.IntField(required=True)
    comment = db.StringField()
    updated = db.DateTimeField()
    created = db.DateTimeField()
    meta = {
    	'indexes': ['organization', 'project', 'email', 'user', 'referring_user']
    }
