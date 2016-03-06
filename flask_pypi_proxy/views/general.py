# -*- coding: utf-8 -*-
import os
import os.path
from urlparse import urljoin
from contextlib import closing
from flask import (
    Blueprint, render_template, request, Response, stream_with_context)
import requests

from flask_pypi_proxy.ext import pypi

mod = Blueprint('general', __name__)


@mod.before_request
def before_request():
    print 'before request'


def generate():
    url = urljoin(pypi.base_url, request.path)
    with closing(requests.get(url, stream=True)) as r:
        for data in r:
            yield data


@mod.route('/simple/')
def simple():
    packages = []
    for filename in os.listdir(pypi.base_folder_path):
        if filename == '.gitignore':
            continue
        packages.append(filename)

    packages.sort()
    return render_template('simple.html', packages=packages)


@mod.route('/simple/<package_name>/')
def package_name(package_name):
    return Response(stream_with_context(generate()))


@mod.route('/packages/<package_type>/<letter>/<package_name>/<package_file>',
           methods=['GET'])
def packages(package_type, letter, package_name, package_file):
    egg_filename = os.path.join(pypi.base_folder_path,
                                package_name,
                                package_file)
    if os.path.exists(egg_filename):
        return 'exist'
    return Response(stream_with_context(generate()))
