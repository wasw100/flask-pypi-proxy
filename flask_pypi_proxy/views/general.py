# -*- coding: utf-8 -*-
import os
import os.path
from urlparse import urljoin
from contextlib import closing
from flask import (
    Blueprint, render_template, request, Response)
import requests

from flask_pypi_proxy.ext import pypi

mod = Blueprint('general', __name__)


@mod.route('/simple/')
def simple():
    packages = []
    for filename in os.listdir(pypi.base_folder_path):
        if filename == '.gitignore':
            continue
        packages.append(filename)

    packages.sort()
    return render_template('simple.html', packages=packages)


@mod.route('/packages/<package_type>/<letter>/<package_name>/<package_file>',
           methods=['GET'])
def packages(package_type, letter, package_name, package_file):
    egg_filename = os.path.join(pypi.base_folder_path,
                                package_name,
                                package_file)
    if os.path.exists(egg_filename):
        # 直接从本地下载
        def file_generate():
            with open(egg_filename, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    yield data
        return Response(file_generate())

    package_path = os.path.join(pypi.base_folder_path, package_name)
    if not os.path.exists(package_path):
        os.makedirs(package_path)

    url = urljoin(pypi.base_url, request.path)

    def generate():
        with closing(requests.get(url, stream=True)) as r:
            with open(egg_filename, 'wb') as f:
                for data in r:
                    f.write(data)
                    yield data
    return Response(generate())
