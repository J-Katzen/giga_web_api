# -*- coding: utf-8 -*-
from giga_web import db
from .organization import Organization
from .user import User


class Post(db.EmbeddedDocument):
    title = db.StringField()
    published = db.DateTimeField()
    updated = db.DateTimeField()
    content = db.StringField()
    tags = db.ListField(db.StringField())
    author = db.ReferenceField(User)


class Project(db.Document):
    name = db.StringField()
    creator = db.ReferenceField(User)
    twitter_hash = db.StringField()
    video_url = db.StringField()
    logo_url = db.StringField()
    description = db.StringField()
    total_raised = db.IntField(default=0)
    total_goal = db.IntField(default=0)
    tags = db.ListField(db.StringField())
    organization = db.ReferenceField(Organization)
    perma_name = db.StringField(unique_with='organization')
    pledge_start_date = db.DateTimeField()
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    fulfilled = db.DateTimeField()
    donor_list = db.ListField(db.ReferenceField(User))
    updates = db.EmbeddedDocumentField(Post)
    meta = {
        'indexes': ['organization', 'creator']
    }
