# -*- coding: utf-8 -*-
from flask import Flask
from flask_pypi_proxy.ext import pypi
from flask_pypi_proxy.views import simple

app = Flask(__name__)
app.config.from_object('config')


# pypi init
pypi.init_app(app)


app.register_blueprint(simple.mod)
