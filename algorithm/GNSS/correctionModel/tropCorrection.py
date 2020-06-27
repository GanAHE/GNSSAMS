#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:单用户对流层延迟改正

@author: GanAH  2019/12/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from database.database import Database
import math


def standardMeteorologicalMethod(H):
    """
    标准气象改正法
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
