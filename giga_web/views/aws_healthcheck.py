# -*- coding: utf-8 -*-

from giga_web import giga_web

app = giga_web


@app.route("/_hostmanager/healthcheck", methods=['GET'])
def aws_healthcheck():
    return 'Pong!'
