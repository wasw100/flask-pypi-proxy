# -*- coding: utf-8 -*-
from urlparse import urljoin
from contextlib import closing
from flask import Blueprint, request, Response, stream_with_context
import requests

from flask_pypi_proxy.ext import pypi

mod = Blueprint('simple', __name__, url_prefix='/simple')


def generate():
    url = urljoin(pypi.base_url, request.path)
    with closing(requests.get(url, stream=True)) as r:
        for data in r:
            yield data


@mod.route('/<package_name>/')
def package(package_name):
    return Response(stream_with_context(generate()))
