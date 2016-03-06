# -*- coding: utf-8 -*-
import os.path

__all__ = (
    'pypi',
)


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
            folder_path = os.path.join(app.config.root_path, '../eggs')
            self.base_folder_path = os.path.abspath(folder_path)

pypi = PypiBase()
