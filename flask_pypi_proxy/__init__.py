# -*- coding: utf-8 -*-
import os
import os.path
from contextlib import closing
from urlparse import urljoin
import requests
from flask import Flask, request, Response, render_template
from flask_pypi_proxy.ext import pypi

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


@app.route('/simple/')
def simple():
    packages = []
    for filename in os.listdir(pypi.base_folder_path):
        if filename == '.gitignore':
            continue
        packages.append(filename)

    packages.sort()
    return render_template('simple.html', packages=packages)


@app.route('/packages/<package_type>/<letter>/<package_name>/<package_file>',
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
