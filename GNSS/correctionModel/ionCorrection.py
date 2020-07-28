#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:电离层延迟改正

@author: GanAH  2019/12/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

import numpy as np
from database.database import Database


def klobuchar(el, UTCTime, position, satellite, alphaList, betaList, ellipsoid):
    """
     Klobuchar 改正模型

     :param el:卫星高度角
     :param UT:当地时间UT时
    :param alphaList:长度为4 从导航电文获取
    :param betaList:长度为4 从导航电文获取
    :return: Tg_DOT 电离层时延
    """
    """
    #待确定参数
    卫星方位角a
    测站P的地心纬度fia_P,地心经度lambda_P
    """
    elli = _ellipsoid(ellipsoid)

    B_pos, L_pos, H_pos = coordinationTran.CoordinationTran(ellipsoid).XYZ_to_BLH(position)
    fia_P = np.arctan((1 - elli.e1 ** 2) * np.tan(B_pos))
    lambda_P = L_pos

    B_sat, L_sat, H_sat = XYZ2BLH(satellite[0, 0], satellite[1, 0], satellite[2, 0], elli)
    a = np.arctan(np.tan(L_sat - L_pos) / np.sin(B_pos))
    print("方位角", a)

    # 测站与P’的地心夹角 单位：度
    EA = 445 / (el + 20) - 4

    # 交点P'的地心纬度
    fia_P_DOT = fia_P + EA * np.cos(a)
    lambda_P_DOT = lambda_P + EA * np.sin(a) / np.cos(fia_P)

    # P'的地方时
    UT = UTCTime[3] + UTCTime[4] / 60.0 + UTCTime[5] / 3600.0
    t = UT + lambda_P_DOT / 15

    # 从数据库获取磁北极坐标，计算P'的地磁纬度fia_m
    fia_earth, lambda_earth = Database.earth_N_pole_coor
    fia_m = fia_P_DOT + (90 - fia_earth) * np.cos(lambda_P_DOT - lambda_earth)

    # 计算振幅和周期
    A = 0
    P = 0
    for i in range(4):
        A += alphaList[i] * (fia_m ** i)
        P += betaList[i] * (fia_m ** i)
    Tg = 5E-9 + A * np.cos(2 * np.pi / P) * (t - 14)
    secZ = 1 + 2 * (((96-el) / 90) ** 3)
    Tg_DOT = secZ * Tg
    return Tg_DOT

def XYZ2BLH(x, y, z, ellipsoid):
    """
    This function converts 3D cartesian coordinates to geodetic coordinates
    """
    # ellipsoid = _ellipsoid(ellipsoid)  # create an ellipsoid instance
    L = np.arctan2(y, x)
    p = np.sqrt(x ** 2 + y ** 2)
    N_init = ellipsoid.a  # initial value of prime vertical radius N
    H_init = np.sqrt(x ** 2 + y ** 2 + z ** 2) - np.sqrt(ellipsoid.a * ellipsoid.b)
    B_init = np.arctan2(z, (1 - N_init * ellipsoid.e1 ** 2 / (N_init + H_init)) * p)
    while True:
        N = ellipsoid.a / np.sqrt(1 - (ellipsoid.e1 ** 2 * np.sin(B_init) ** 2))
        H = (p / np.cos(B_init)) - N
        B = np.arctan2(z, (1 - N * ellipsoid.e1 ** 2 / (N + H)) * p)
        if np.abs(B_init - B) < 1e-8 and np.abs(H_init - H) < 1e-8:
            break
        B_init = B
        H_init = H
    return B, L, H

def _ellipsoid(ellipsoidName):
    axes = {'GRS80': [6378137.000, 6356752.314140],
            'WGS84': [6378137.000, 6356752.314245],
            'Hayford': [6378388.000, 6356911.946000]}[ellipsoidName]
    a, b = axes[0], axes[1]
    return _Ellipsoid(a, b)

class _Ellipsoid:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.f = (a - b) / a
        self.e1 = np.sqrt((a ** 2 - b ** 2) / a ** 2)
        self.e2 = np.sqrt((a ** 2 - b ** 2) / b ** 2)




