from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError
from base64 import urlsafe_b64encode, urlsafe_b64decode
from bson.objectid import ObjectId
from bson.errors import InvalidId


class ObjectIDConverter(BaseConverter):

    def to_python(self, value):
        try:
            return ObjectId(urlsafe_b64decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return urlsafe_b64encode(value.binary)
