# -*- coding: utf-8 -*-
import os
import os.path
import hashlib
import re
from contextlib import closing
import logging
from logging.handlers import RotatingFileHandler
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import requests

from flask import Flask, request, Response, render_template, make_response
from utils import get_package_name

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    log_path = os.path.join(app.root_path, 'web.log')
    handler = RotatingFileHandler(log_path, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


class PypiBase(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        # set base_url
        self.base_url = app.config.get('PYPI_BASE_URL',
                                       'https://pypi.python.org')
        # set base folder path
        self.base_folder_path = app.config.get('PYPI_BASE_FOLDER_APTH')
        if not self.base_folder_path:
            folder_path = os.path.join(app.config.root_path, 'eggs')
            self.base_folder_path = os.path.abspath(folder_path)

pypi = PypiBase(app)


@app.before_request
def before_request():
    if request.method != 'GET' or request.endpoint in app.view_functions:
        return
    url = urljoin(pypi.base_url, request.path)

    r = requests.get(url, stream=True)
    return Response(r, status=r.status_code,
                    content_type=r.headers.get('content-type'))


@app.route('/simple')
@app.route('/simple/')
def simple():
    packages = []
    for filename in os.listdir(pypi.base_folder_path):
        if filename == '.gitignore':
            continue
        packages.append(filename)

    packages.sort()
    return render_template('simple.html', packages=packages)


_PACKET_PARTERN = re.compile(r'/([\w\-\.]+)#md5=(\w+)')


@app.route('/simple/<package_name>')
@app.route('/simple/<package_name>/')
def simple_package(package_name):
    url = urljoin(pypi.base_url, request.path)
    r = requests.get(url)
    if r.status_code != 200:
        return make_response(r.text, r.status_code)

    pd = dict()
    for name, md5 in _PACKET_PARTERN.findall(r.text):
        pd[name] = md5
    # 对比本地, md5错误则删除本地
    package_folder = os.path.join(pypi.base_folder_path, package_name)
    if os.path.exists(package_folder):
        for filename in os.listdir(package_folder):
            if filename.endswith('.md5'):
                continue
            egg_file = os.path.join(package_folder, filename)
            md5_file = os.path.join(package_folder, '{0}.md5'.format(filename))
            if os.path.exists(md5_file):
                with open(md5_file, 'rb') as f:
                    md5 = f.read()
            else:
                md5 = 'no md5 file'

            if md5 != pd.get(filename):
                os.remove(egg_file)
                app.logger.error('delete file %s', egg_file)

    return r.text


@app.route('/packages/<package_type>/<letter>/<package_name>/<package_file>',
           methods=['GET'])
def packages(package_type, letter, package_name, package_file):
    package_name = get_package_name(package_file) or package_name.lower()
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
        m = hashlib.md5()
        with open(egg_filename, 'wb') as f:
            with closing(requests.get(url, stream=True)) as r:
                for data in r:
                    m.update(data)
                    f.write(data)
                    yield data
        # 计算md5
        md5 = m.hexdigest()
        with open('{0}.md5'.format(egg_filename), 'w') as f:
            f.write(md5)
        return

    return Response(generate())
