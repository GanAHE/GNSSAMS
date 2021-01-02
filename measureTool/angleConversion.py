#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:角度转换类

@author: GanAH  2020/2/18.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math


class Angle():
    # 类属性，总感觉定义怪怪的，分秒像时间系统一样，嗯！
    _degree = 0
    _minute = 0
    _second = 0

    def __init__(self, degree, minute=0, second=0):
        """
        构造函数
        :param degree: 必要参数
        :param minute: 可选参数
        :param second: 可选参数
        """
        self._degree = degree
        self._minute = minute
        self._second = second

    def degreeToMinute(self):
        return self._degree * 60

    def degreeToSecond(self):
        return self._degree * 3600

    def degreeToDMS(self):
        D = int(self._degree)
        temp = self._degree - D
        M = int(temp * 60)
        S = int((temp * 60 - M) * 60)
        # 本转换类的扩展适应性
        M = M + self._minute
        S = S + self._second
        # 分秒数值控制
        if S >= 60:
            S = S - 60
            M = M + 1
        if M >= 60:
            M = M - 60
            D = D + 1

        return [D, M, S]

    def DMSToDegree(self):
        return self._degree + self._minute / 60 + self._second / 3600
    def toRadian(self):
        return self.DMSToDegree()*math.pi/180