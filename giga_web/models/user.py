# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization


class School(db.EmbeddedDocument):
    name = db.StringField()
    class_year = db.IntField()
    major = db.StringField()
    minor = db.StringField()
    organization = db.ReferenceField(Organization)


class User(db.Document):
    email = db.EmailField(unique=True, required=True)
    firstname = db.StringField()
    lastname = db.StringField()
    password = db.StringField()
    verified = db.BooleanField(default=False)
    facebook_id = db.StringField()
    twitter_id = db.StringField()
    avatar_url = db.URLField()
    phone = db.StringField()
    education = db.ListField(db.EmbeddedDocumentField(School))
    updated = db.DateTimeField()
    meta = {
    	'indexes': ['email']
    }

# queries!
# User.objects(education__organization=o) where o is organization object or objectid
