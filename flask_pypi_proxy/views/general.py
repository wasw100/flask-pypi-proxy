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
        return 'exist'

    # TODO: 从pypi网站下载并保存到本地
    url = urljoin(pypi.base_url, request.path)
    with closing(requests.get(url, stream=True)) as r:
        return Response(r)
