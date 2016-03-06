#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_pypi_proxy import app

__all__ = ('app')


if __name__ == '__main__':
    app.run(port=8007)
