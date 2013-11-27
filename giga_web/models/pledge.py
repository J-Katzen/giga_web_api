# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization
from .user import User
from .project import Project


class Pledge(db.Document):
    organization = db.ReferenceField(Organization)
    project = db.ReferenceField(Project)
    user = db.ReferenceField(User)
    amount = db.IntField()
    meta = {
    	'indexes': ['organization', 'project', 'user']
    }
