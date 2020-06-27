#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 边角精度匹配测探

@author: GanAH  2020/5/16.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math


def CAM(a, b, S, mr):
    """
    边角精度匹配计算
    :param a: 固定误差
    :param b: 比例误差
    :param S: 边长
    :param mr: 方向中误差,单位为秒（″）
    :return: list[matchCode: 1 完全匹配 | 0 基本匹配 | -1 不匹配,横向误差：mq,纵向误差：ml]
    """
    mq = mr * S / 206265
    ml = math.sqrt(a * a + (b * S) * (b * S))
    if abs(mq - ml) < 1.0E-6:
        print("精度匹配")
        return [1, mq, ml]

    else:
        k = 0.1
        while True:
            if k >= 3:
                return [-1, mq, ml]
            s1 = ml / k
            s2 = k * mq
            k += 0.2
            if s1 <= mq and mq <= s2:
                print("精度基本匹配")
                return [0, mq, ml]




print(CAM(0.00003,6E-9,260,0.362))
