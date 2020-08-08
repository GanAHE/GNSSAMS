#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 坐标转换类

@author: GanAH  2020/2/10.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from numpy import sin, cos, tan, arctan2, sqrt, arctan, mat

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
        """
        BLH转XYZ
        :param BLH: 大地坐标系坐标 B(rad),L(rad),H(m)
        :return: X(m),Y(m),Z(m)
        """
        N = self.ellipsis.c / sqrt(1 + (self.ellipsis.dot_e ** 2) * (cos(BLH[0]) ** 2))
        X = (N + BLH[2]) * cos(BLH[0]) * cos(BLH[1])
        Y = (N + BLH[2]) * cos(BLH[0]) * sin(BLH[1])
        Z = (N * (1 - self.ellipsis.e ** 2) + BLH[2]) * sin(BLH[0])
        return X, Y, Z

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
        # k = 1 - self.ellipsis.dot_e * self.ellipsis.dot_e + 1
        k = 1 + self.ellipsis.dot_e * self.ellipsis.dot_e
        while abs(ti_1 - ti) > 1e-6:
            ti_1 = ti
            ti = to + P * ti / sqrt(k + ti * ti)
        B = arctan(ti)
        # N = self.ellipsis.a / sqrt(1 - self.ellipsis.e * self.ellipsis.e * sin(B) * sin(B))
        N = self.ellipsis.c / sqrt(1 + self.ellipsis.dot_e * self.ellipsis.dot_e * cos(B) * cos(B))
        H = sqrt_XY / cos(B) - N

        return B, L, H

    def XYZ_to_NEH(self, XYZ, centerXYZ):
        """
        XYZ转NEH
        :param XYZ: X(m),Y(m),Z(m)
        :param centerXYZ: 站心坐标X(m),Y(m),Z(m)
        :return:
        """
        centerB, centerL, centerH = self.XYZ_to_BLH(centerXYZ)
        trans = [[(-1 * sin(centerB) * cos(centerL)), (-1 * sin(centerB) * sin(centerL)), (cos(centerB))],
                 [(-1 * sin(centerL)),                (cos(centerL)),                     0],
                 [(cos(centerB) * cos(centerL)),      (cos(centerB) * sin(centerL)),      (sin(centerB))]]
        deltaXYZ = [[XYZ[0] - centerXYZ[0]],
                    [XYZ[1] - centerXYZ[1]],
                    [XYZ[2] - centerXYZ[2]]]
        NEH = mat(trans) * mat(deltaXYZ)
        N = NEH[0][0]
        E = NEH[1][0]
        H = NEH[2][0]
        return N, E, H


    def NEH_to_XYZ(self, NEH, centerXYZ):
        """
        NEU转XYZ
        :param NEH:
        :param centerXYZ: 站心坐标X(m),Y(m),Z(m)
        :return:
        """
        centerB, centerL, centerH = self.XYZ_to_BLH(centerXYZ)
        trans = [[(-1 * sin(centerB) * cos(centerL)), (-1 * sin(centerL)), (cos(centerB) * cos(centerL))],
                 [(-1 * sin(centerB) * sin(centerL)), (cos(centerL)),      (cos(centerB) * sin(centerL))],
                 [(cos(centerB)),                     0,                   (sin(centerB))]]
        NEH_mat = [[NEH[0]],
                   [NEH[1]],
                   [NEH[2]]]
        center = [[centerXYZ[0]],
                  [centerXYZ[1]],
                  [centerXYZ[2]]]
        XYZ = mat(center) + mat(trans) * mat(NEH_mat)
        X = XYZ[0][0]
        Y = XYZ[1][0]
        Z = XYZ[2][0]
        return X, Y, Z

    def BLH_to_NEH(self, BLH,centerXYZ):
        """
        BLH 转 NEH
        <p> 中转
        :param BLH:
        :return:
        """
        return self.XYZ_to_NEH(self.BLH_to_XYZ(BLH), centerXYZ)

    def NEH_to_BLH(self, NEH,centerXYZ):
        self.XYZ_to_BLH(self.NEH_to_XYZ(NEH, centerXYZ))


