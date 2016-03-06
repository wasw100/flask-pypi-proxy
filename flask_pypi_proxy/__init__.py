# -*- coding: utf-8 -*-
from contextlib import closing
from urlparse import urljoin
import requests
from flask import Flask, request, Response
from flask_pypi_proxy.ext import pypi
from flask_pypi_proxy.views import general

app = Flask(__name__)
app.config.from_object('config')


# pypi init
pypi.init_app(app)


# before request
@app.before_request
def before_request():
    if request.method != 'GET' or request.endpoint in app.view_functions:
        return
    url = urljoin(pypi.base_url, request.path)

    with closing(requests.get(url, stream=True)) as r:
        resp_headers = []
        for name, value in r.headers.items():
            if name.lower() in ('content-length', 'connection',
                                'content-encoding'):
                continue
            resp_headers.append((name, value))
        return Response(r, status=r.status_code,
                        content_type=r.headers.get('content-type'))


app.register_blueprint(general.mod)
