from flask import Flask
from converter import ObjectIDConverter

giga_web = Flask(__name__)
giga_web.url_map.converters['objectid'] = ObjectIDConverter
crud_url = 'http://giga-eve.elasticbeanstalk.com'

from giga_web import views
