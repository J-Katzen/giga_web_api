
# -*- coding: utf-8 -*-
from giga_web import db
from .project import Project

STATUSES = ('not contacted', 'converted', 'pledged', 'maybe', 'no')

class Contact(db.EmbeddedDocument):
    con_id = db.ObjectIdField(required=True)
    email = db.EmailField(required=True)
    owners = db.ListField(db.EmailField())
    fullname = db.StringField()
    phone = db.StringField()
    donated = db.IntField()
    updated = db.DateTimeField()
    status = db.StringField(choices=STATUSES, default='not contacted')

class MarketingList(db.Document):
    project = db.ReferenceField(Project, required=True)
    contacts = db.ListField(db.EmbeddedDocumentField(Contact))
    convert_conversion = db.IntField(default=0)
    total_donated = db.IntField(default=0)
    updated = db.DateTimeField()
    meta = {
        'indexes': ['project']
    }
