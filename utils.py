# -*- coding: utf-8 -*-
import re


PACKAGE_PATTERN = re.compile('(.*)?-\d+\.\d+\.')


def get_package_name(filename):
    """通过package filename获取package_name"""
    m = PACKAGE_PATTERN.match(filename)
    if m:
        return m.group(1).lower()
