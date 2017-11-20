# -*- coding: utf-8 -*-
__author__='victorz'
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()