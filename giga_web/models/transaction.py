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
    total_amt = db.IntField()
    giga_fee = db.IntField()
    trans_fee = db.IntField()
    comment = db.StringField()
    meta = {
    	'indexes': ['organization', 'user', 'project', 'referring_user']
    }
