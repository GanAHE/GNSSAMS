#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 椭球参数类

@author: GanAH  2020/7/25.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


class Ellipsoid(object):
    def __init__(self, WGS84=None, CGCS2000=None, internationalEllipsoid_1975=None, krasovskiEllipsoid=None,
                 userPrivateEllipsoid=None):
        self.WGS84 = WGS84
        self.CGCS2000 = CGCS2000
        self.internationalEllipsoid_1975 = internationalEllipsoid_1975
        self.krasovskiEllipsoid = krasovskiEllipsoid
        self.userPrivateEllipsoid = userPrivateEllipsoid


class WGS84(object):
    def __init__(self,paraList):
        self.a = paraList[0]
        self.b = paraList[1]
        # 扁率α
        self.alpha = paraList[2]
        self.e = paraList[3]
        self.dot_e = paraList[4]
        self.c = self.a * self.a / self.b


class CGCS2000(object):
    def __init__(self,paraList):
        self.a = paraList[0]
        self.b = paraList[1]
        # 扁率α
        self.alpha = paraList[2]
        self.e = paraList[3]
        self.dot_e = paraList[4]
        self.c = self.a * self.a / self.b


class internationalEllipsoid_1975(object):
    def __init__(self,paraList):
        self.a = paraList[0]
        self.b = paraList[1]
        # 扁率α
        self.alpha = paraList[2]
        self.e = paraList[3]
        self.dot_e = paraList[4]
        self.c = self.a * self.a / self.b


class krasovskiEllipsoid(object):
    def __init__(self,paraList):
        self.a = paraList[0]
        self.b = paraList[1]
        # 扁率α
        self.alpha = paraList[2]
        self.e = paraList[3]
        self.dot_e = paraList[4]
        self.c = self.a * self.a / self.b


class userPrivateEllipsoid(object):
    def __init__(self, paraList):
        self.a = paraList[0]
        self.b = paraList[1]
        # 扁率α
        self.alpha = paraList[2]
        self.e = paraList[3]
        self.dot_e = paraList[4]
        self.c = self.a * self.a / self.b