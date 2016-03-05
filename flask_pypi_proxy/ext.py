# -*- coding: utf-8 -*-
__all__ = (
    'pypi',
)


class Pypi(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.base_url = app.config.get('PYPI_BASE_URL',
                                       'http://pypi.python.org')

pypi = Pypi()
