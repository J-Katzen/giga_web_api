# -*- coding: utf-8 -*-
from giga_web import db


class OrgStripeInfo(db.EmbeddedDocument):
    stripe_id = db.StringField(unique=True)
    access_token = db.StringField()
    publishable_key = db.StringField()
    refresh_token = db.StringField()


class Organization(db.Document):
    name = db.StringField()
    header_url = db.URLField()
    perma_name = db.StringField(unique=True, required=True)
    logo_url = db.URLField()
    org_type = db.StringField()
    giga_fee_percent = db.IntField(default=500)
    giga_fee_cents = db.IntField(default=0)
    trans_fee_percent = db.IntField(default=290)
    trans_fee_cents = db.IntField(default=30)
    claimed = db.BooleanField(default=False)
    stripe_info = db.EmbeddedDocumentField(OrgStripeInfo)
    total_raised = db.IntField(default=0)
    updated = db.DateTimeField()
    meta = {
        'indexes': ['perma_name']
    }
