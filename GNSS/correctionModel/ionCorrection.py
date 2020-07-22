#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:电离层延迟改正

@author: GanAH  2019/12/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math
from database.database import Database


def klobuchar(el, UT, alphaList, betaList):
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
    a = 0
    fia_P = 0
    lambda_P = 0

    # 测站与P’的地心夹角 单位：度
    EA = 445 / (el + 20) - 4

    # 交点P'的地心纬度
    fia_P_DOT = fia_P + EA * math.cos(a)
    lambda_P_DOT = lambda_P + EA * math.sin(a) / math.cos(fia_P)

    # P'的地方时
    t = UT + lambda_P_DOT / 15

    # 从数据库获取磁北极坐标，计算P'的地磁纬度fia_m
    fia_earth, lambda_earth = Database.earth_N_pole_coor
    fia_m = fia_P_DOT + 10.07 * math.cos(lambda_P_DOT - 288.04)

    # 计算振幅和周期
    A = 0
    P = 0
    for i in range(4):
        A += alphaList[i] * (fia_m ** i)
        P += betaList[i] * (fia_m ** i)
    Tg = 5E-9 + A * math.cos(2 * math.pi / P) * (t - 14)
    secZ = 1 + 2 * (((96-el) / 90) ** 3)
    Tg_DOT = secZ * Tg
    return Tg_DOT



