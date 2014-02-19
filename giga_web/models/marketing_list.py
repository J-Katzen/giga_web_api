# -*- coding: utf-8 -*-
from giga_web import db
from .user import User
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
    pledge_conversion = db.IntField()
    convert_conversion = db.IntField()
    total_donated = db.IntField()
    owner = db.ReferenceField(User)
