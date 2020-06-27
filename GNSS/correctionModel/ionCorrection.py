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


def klobuchar(el, UT, h, aList, beidaList):
    """
     Klobuchar 改正模型

     :param el:卫星高度角
     :param UT:当地时间UT时
     :param h: 未知参数
    :param aList:长度为3 从导航电文获取？？
    :param beidaList:长度为3 从导航电文获取？？
    :return: Tg_DOT 电离层时延
    """
    # 测站与P’的地心夹角 单位：度
    EA = 445 / (el + 20) - 4
    """
    #待确定参数
    卫星方位角a
    测站P的地心维度fia_P,地心经度lambda_P
    """
    a = 0
    fia_P = 0
    lambda_P = 0
    # 交点P'的地心维度
    fia_P_DOT = fia_P + EA * math.cos(a)
    lambda_P_DOT = lambda_P + EA * math.sin(a) / math.cos(fia_P)

    # P'的地方时
    t = UT + lambda_P_DOT / 15
    # 从数据库获取磁北极坐标，计算P'的地磁维度fia_m
    fia_earth, lambda_earth = Database.earth_N_pole_coor
    fia_m = fia_P_DOT + 10.07 * math.cos(lambda_P_DOT - 288.04)

    # 计算振幅和周期
    A = 0
    P = 0
    for i in range(3):
        A += aList[i] * (fia_m ** i)
        P += beidaList[i] * (fia_m ** i)
    Tg = 5E-9 + A * math.cos(2 * math.pi * (t - 14 ** h) / P)
    Tg_DOT = Tg * (1 + 2 * ((96 - el) / 90) * ((96 - el) / 90) * ((96 - el) / 90))
    return Tg_DOT



