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


class Reward(db.EmbeddedDocument):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    cost = db.IntField(required=True)
    quantity = db.IntField(required=True)


class Project(db.Document):
    name = db.StringField(required=True)
    creator = db.ReferenceField(User)
    twitter_hash = db.StringField()
    video_url = db.URLField()
    logo_url = db.URLField()
    description = db.StringField()
    total_raised = db.IntField(default=0)
    total_goal = db.IntField(default=0)
    total_giga_fee = db.IntField(default=0)
    total_trans_fee = db.IntField(default=0)
    total_net_raised = db.IntField(default=0)
    rewards = db.ListField(db.EmbeddedDocumentField(Reward))
    tags = db.ListField(db.StringField())
    organization = db.ReferenceField(Organization)
    perma_name = db.StringField(unique_with='organization')
    pledge_start_date = db.DateTimeField()
    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    fulfilled = db.DateTimeField()
    donor_list = db.ListField(db.ReferenceField(User))
    update_posts = db.ListField(db.EmbeddedDocumentField(Post))
    updated = db.DateTimeField()
    meta = {
        'indexes': ['organization', 'creator']
    }
