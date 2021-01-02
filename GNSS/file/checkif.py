#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/7/15.
@version 1.0.
@contact: dgzc159@163.com
"""

import os
from patoolib import extract_archive
import http.client


def isfloat(value):
    """ To check if any variable can be converted to float or not """
    try:
        float(value)
        return True
    except ValueError:
        return False

def isint(value):
    """ To check if any variable can be converted to integer """
    try:
        int(value)
        return True
    except ValueError:
        return False

def check_internet():
    """ To check if there is an internet connection for FTP downloads """
    connection = http.client.HTTPConnection("www.google.com", timeout=5)
    try:
        connection.request("HEAD", "/")
        connection.close()
        return True
    except:
        connection.close()
        return False

