# -*- coding: utf-8 -*-
from giga_web import db
from .project import Project

STATUSES = ('not contacted', 'converted', 'pledged', 'maybe', 'no')

class Contact(db.EmbeddedDocument):
    email = db.EmailField(required=True)
    owners = db.ListField(db.EmailField())
    fullname = db.StringField()
    phone = db.StringField()
    converted = db.BooleanField()
    donated = db.IntField()
    status = db.StringField(choices=STATUSES, default='not contacted')

class MarketingList(db.Document):
    project = db.ReferenceField(Project, required=True)
    contacts = db.ListField(db.EmbeddedDocumentField(Contact))
    pledge_conversion = db.IntField(default=0)
    convert_conversion = db.IntField(default=0)
    total_donated = db.IntField(default=0)
