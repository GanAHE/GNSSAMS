#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:单用户对流层延迟改正

@author: GanAH  2019/12/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import datetime

from database.database import Database
import math
import numpy as np


def standardMeteorologicalMethod(H):
    """
    标准气象改正法
    <p>对流层延迟
    :param H: 测站高程
    :return: 改正后的对流层时延 ，Vtrop = -f(n-1)ds
    """
    # 从内部数据储存中获取标准气象元素值
    listElement = Database.standardMeteorologicalElement
    To = listElement[0]
    Po = listElement[1]
    RHo = listElement[2]

    T = To - 0.0065 * H
    P = Po * ((1 - 0.0000266 * H) ** 5.225)
    e = RHo * math.exp(-0.0006396 * H - 37.2465 + 0.213166 * T - 0.00026908 * T * T)

    # 大气折射指数
    N = 77.6 * P / T + 3.73E5 * e / (T * T)

    Vtrop = N * 1E-6
    return Vtrop


def tropospheric_delay(x, y, z, elevation, epoch):
    """
    Colins（1999）方法
    <p1>对流层延迟
    <p2>
    :param x: 坐标
    :param y:
    :param z:
    :param elevation: 卫星仰角
    :param epoch: 历元
    :return: 对流层延迟 单位：m
    """
    """
    Calculates tropospheric delay using Colins(1999) method
    Input:
        Cartesian coordinates of receiver in ECEF frame (x,y,z)
        Elevation Angle [unit: degree] of satellite vehicle
    Output:
        Tropospheric delay [unit: m]

    Reference:
    Collins, J. P. (1999). Assessment and Development of a Tropospheric Delay Model for
    Aircraft Users of the Global Positioning System. M.Sc.E. thesis, Department of
    Geodesy and Geomatics Engineering Technical Report No. 203, University of
    New Brunswick, Fredericton, New Brunswick, Canada, 174 pp
    """
    lat, lon, ellHeight = XYZ2BLH(x, y, z)
    ortHeight = ellHeight  # Using elliposidal height for now
    # --------------------
    # constants
    k1 = 77.604  # K/mbar
    k2 = 382000  # K^2/mbar
    Rd = 287.054  # J/Kg/K
    g = 9.80665  # m/s^2
    gm = 9.784  # m/s^2
    # --------------------
    # linear interpolation of meteorological values
    # Average values
    ave_params = np.array([
        [1013.25, 299.65, 26.31, 6.30e-3, 2.77],
        [1017.25, 294.15, 21.79, 6.05e-3, 3.15],
        [1015.75, 283.15, 11.66, 5.58e-3, 2.57],
        [1011.75, 272.15, 6.78, 5.39e-3, 1.81],
        [1013.00, 263.65, 4.11, 4.53e-3, 1.55]
    ])
    # seasonal variations
    sea_params = np.array([
        [0.00, 0.00, 0.00, 0.00e-3, 0.00],
        [-3.75, 7.00, 8.85, 0.25e-3, 0.33],
        [-2.25, 11.00, 7.24, 0.32e-3, 0.46],
        [-1.75, 15.00, 5.36, 0.81e-3, 0.74],
        [-0.50, 14.50, 3.39, 0.62e-3, 0.30]
    ])
    # Latitude index
    Latitude = np.linspace(15, 75, 5)
    if abs(lat) <= 15.0:
        indexLat = 0
    elif 15 < abs(lat) <= 30:
        indexLat = 1
    elif 30 < abs(lat) <= 45:
        indexLat = 2
    elif 45 < abs(lat) <= 60:
        indexLat = 3
    elif 60 < abs(lat) < 75:
        indexLat = 4
    elif 75 <= abs(lat):
        indexLat = 5
    # ----------------
    if indexLat == 0:
        ave_meteo = ave_params[indexLat, :]
        sea_meteo = sea_params[indexLat - 1, :]
    elif indexLat == 5:
        ave_meteo = ave_params[indexLat - 1, :]
        sea_meteo = sea_params[indexLat - 1, :]
    else:
        ave_meteo = ave_params[indexLat - 1, :] + (ave_params[indexLat, :] - ave_params[indexLat - 1, :]) * (
                abs(lat) - Latitude[indexLat - 1]) / (Latitude[indexLat] - Latitude[indexLat - 1])
        sea_meteo = sea_params[indexLat - 1, :] + (sea_params[indexLat, :] - sea_params[indexLat - 1, :]) * (
                abs(lat) - Latitude[indexLat - 1]) / (Latitude[indexLat] - Latitude[indexLat - 1])
    # --------------------
    doy = datetime2doy(epoch, string=False)
    if lat >= 0.0:  # northern hemisphere
        doy_min = 28
    else:  # southern latitudes
        doy_min = 211
    param_meteo = ave_meteo - sea_meteo * np.cos((2 * np.pi * (doy - doy_min)) / 365.25)
    pressure, temperature, e, beta, lamda = param_meteo[0], param_meteo[1], param_meteo[2], param_meteo[3], param_meteo[
        4]
    # --------------------
    ave_dry = 1e-6 * k1 * Rd * pressure / gm
    ave_wet = 1e-6 * k2 * Rd / (gm * (lamda + 1) - beta * Rd) * e / temperature
    d_dry = ave_dry * (1 - beta * ortHeight / temperature) ** (g / Rd / beta)
    d_wet = ave_wet * (1 - beta * ortHeight / temperature) ** (((lamda + 1) * g / Rd / beta) - 1)
    m_elev = 1.001 / np.sqrt(0.002001 + np.sin(np.deg2rad(elevation)) ** 2)
    Vtrop = (d_dry + d_wet) * m_elev
    return Vtrop


def XYZ2BLH(x, y, z, ellipsoid='GRS80'):
    """
    This function converts 3D cartesian coordinates to geodetic coordinates
    """
    ellipsoid = _ellipsoid(ellipsoid)  # create an ellipsoid instance
    L = np.arctan2(y, x)  # $\lambda = \atan\frac{y}{x}$
    p = np.sqrt(x ** 2 + y ** 2)  # $p = \sqrt{x^2+y^2}$
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
    return np.rad2deg(B), np.rad2deg(L), H


def datetime2doy(now_date, string=False):
    now_year = now_date[0]
    now_month = now_date[1]
    now_day = now_date[2]
    start = datetime.date(now_year, 1, 1)
    now = datetime.date(now_year, now_month, now_day)
    doy = now - start + datetime.timedelta(days=1)
    doy = doy.days
    if string == True:
        doy = str(doy)
        if len(doy) == 1:
            doy = "00" + doy
        elif len(doy) == 2:
            doy = "0" + doy
        else:
            doy = doy
    return doy


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
        self.f = (a - b) / a  # flattening: $f = \frac{a-b}{a}$
        self.e1 = np.sqrt((a ** 2 - b ** 2) / a ** 2)  # first eccentricity  : $e   = \sqrt{\frac{a^2-b^2}{a^2}}$
        self.e2 = np.sqrt((a ** 2 - b ** 2) / b ** 2)  # second eccentricity : $e^' = \sqrt{\frac{a^2-b^2}{b^2}}$
