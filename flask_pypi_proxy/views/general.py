# -*- coding: utf-8 -*-
from urlparse import urljoin
from contextlib import closing
from flask import Blueprint, request, Response, stream_with_context
import requests

from flask_pypi_proxy.ext import pypi

mod = Blueprint('general', __name__)


def generate():
    url = urljoin(pypi.base_url, request.path)
    with closing(requests.get(url, stream=True)) as r:
        for data in r:
            yield data


@mod.route('/simple/<package_name>/')
def package_name(package_name):
    return Response(stream_with_context(generate()))


@mod.route('/packages/<package_type>/<letter>/<package_name>/<package_file>',
                   methods=['GET'])
def packages(package_type, letter, package_name, package_file):
    return Response(stream_with_context(generate()))
