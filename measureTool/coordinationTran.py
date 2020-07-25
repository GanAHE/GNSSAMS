#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 坐标转换类

@author: GanAH  2020/2/10.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from numpy import sin, cos, tan, arctan2, sqrt, arctan

from database.database import Database


class CoordinationTran():
    ellipsis = None
    """
    # 椭球参数说明
    # a，b,e,e^2,
    """

    def __init__(self, elli):
        if elli == "WGS84":
            self.ellipsis = Database.ellipsoid.WGS84
        elif elli == "CGCS2000":
            self.ellipsis = Database.ellipsoid.CGCS2000
        elif elli == "Krasovski":
            self.ellipsis = Database.ellipsoid.krasovskiEllipsoid
        elif elli == "IE1975":
            self.ellipsis = Database.ellipsoid.internationalEllipsoid_1975
        else:
            self.ellipsis = Database.ellipsoid.userPrivateEllipsoid

    """
    坐标系统转换
    传入参数：一维list
    """

    def BLH_to_XYZ(self, BLH):
        pass

    def XYZ_to_BLH(self, XYZ):
        """
        XYZ转BLH
        :param XYZ: 地固坐标系坐标 1*3List
        :return:B(rad)，L(rad)，H(m)
        """
        L = arctan2(XYZ[1], XYZ[0])
        sqrt_XY = sqrt(XYZ[1] * XYZ[1] + XYZ[0] * XYZ[0])
        # 超越方程
        to = XYZ[2] / sqrt_XY
        ti = to
        ti_1 = 0

        P = self.ellipsis.c * self.ellipsis.e * self.ellipsis.e / sqrt_XY
        k = 1 - self.ellipsis.dot_e * self.ellipsis.dot_e + 1
        while abs(ti_1 - ti) > 1e-6:
            ti_1 = ti
            ti = to + P * ti / sqrt(k + ti * ti)
        B = arctan(ti)
        N = self.ellipsis.a / sqrt(1 - self.ellipsis.e * self.ellipsis.e * sin(B) * sin(B))
        H = sqrt_XY / cos(B) - N

        return B, L, H

    def XYZ_to_NEH(self, XYZ):
        pass

    def NEH_to_XYZ(self, NEH):
        pass

    def BLH_to_NEH(self, BLH):
        """
        BLH 转 NEH
        <p> 中转
        :param BLH:
        :return:
        """
        return self.XYZ_to_NEH(self.BLH_to_XYZ(BLH))

    def NEH_to_BLH(self, NEH):
        self.XYZ_to_BLH(self.NEH_to_XYZ(NEH))


