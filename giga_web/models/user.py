# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization


class School(db.EmbeddedDocument):
    name = db.StringField()
    class_year = db.IntField()
    major = db.StringField()
    minor = db.StringField()
    organization = db.ReferenceField(Organization)

class UserStripeInfo(db.EmbeddedDocument):
    stripe_id = db.StringField(unique=True)
    access_token = db.StringField()
    publishable_key = db.StringField()
    refresh_token = db.StringField()

class FBFriend(db.EmbeddedDocument):
    fb_id = db.StringField()
    fb_name = db.StringField()

class User(db.Document):
    email = db.EmailField(unique=True, required=True)
    fullname = db.StringField()
    password = db.StringField()
    phone = db.StringField()
    email_verified = db.BooleanField(default=False)
    phone_verified = db.BooleanField(default=False)
    facebook_id = db.StringField()
    fb_friends = db.ListField(FBFriend)
    avatar_url = db.URLField()
    phone = db.StringField()
    stripe_info = db.EmbeddedDocumentField(UserStripeInfo)
    education = db.ListField(db.EmbeddedDocumentField(School))
    updated = db.DateTimeField()
    roles = db.ListField(db.StringField(), default=['ROLE_USER'])
    meta = {
    	'indexes': ['email']
    }

# queries!
# User.objects(education__organization=o) where o is organization object or objectid
