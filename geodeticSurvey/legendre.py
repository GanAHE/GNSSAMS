#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 勒让德函数

@author: GanAH  2020/7/8.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from math import cos, pi, sqrt

# from geodeticSurvey.gravityFieldModel import GravityModel


class Legendre(object):
    def normalizationLegendre(self, n, m, cos_value):
        """
        完全正规化勒让德函数
        <p> 标准向前列递推法
        :param value: cos(theta)
        :param n: 阶/次
        :param m:
        :return:
        """
        if m < n - 1:
            s1 = self._normalLegendre(cos_value, n, m, 0)
            s2 = self._normalLegendre(cos_value, n, m, 1)
            return s1 - s2
        else:
            return self._normalLegendre(cos_value, n, m)

    def _normalLegendre(self, cos_v, n, m, index=None):
        if m < n - 1:
            if index == 0:
                return sqrt((4 * n * n - 1) / (n * n - m * m)) * cos_v * self.normalizationLegendre(cos_v,
                                                                                                    n - 1,
                                                                                                    m)
            elif index == 1:
                return sqrt(
                    (2 * n + 1) * (n * n - m * m - 2 * n + 1) / (
                            (2 * n - 3) * (n * n - m * m))) * self.normalizationLegendre(cos_v, n - 2, m)
        # 递推初值等
        elif n == 0 and m == 0:
            return 1
        elif n == 1 and m == 0:
            return sqrt(3) * cos_v
        elif m == n and m > 1:
            return sqrt((2 * n + 1) / (2 * n)) * sqrt((1 - cos_v * cos_v)) * self.normalizationLegendre(cos_v, n - 1,
                                                                                                        n - 1)
        elif m == n - 1:
            return sqrt(2 * n + 1) * sqrt((1 - cos_v * cos_v)) * self.normalizationLegendre(cos_v, n - 1, n - 1)
        elif n == 1 and m == 1:
            return sqrt(3) * cos_v
        else:
            print("辅助错误值，该值未处理：", n, m)
            return 1

    def normalizationLegendre_II(self, n, m, cos_v):
        if n > m:
            s1 = self._normalizationLegendre_row(n, m, cos_v, index=0)
            s2 = self._normalizationLegendre_row(n, m, cos_v, index=1)
            return s1 - s2
        else:
            return self._normalizationLegendre_row(n, m, cos_v)

    def _normalizationLegendre_row(self, n, m, cos_v, index=None):
        """
        按行递推法
        :param n: 阶
        :param m: 次
        :param cos_v: cos值
        :return: float
        """
        sin_theta = sqrt(1 - cos_v * cos_v)
        if n > m:
            if m == 0:
                k = 2
            else:
                k = 1
            if index == 0:
                gnm = 2 * (m + 1) / sqrt((n - m) * (n + m + 1))
                return sqrt(1 / k) * (cos_v / sin_theta) * gnm * self.normalizationLegendre_II(n, m + 1, cos_v)
            elif index == 1:
                hnm = sqrt((n + m + 2) * (n - m - 1) / ((n - m) * (n + m + 1)))
                return sqrt(1 / k) * hnm * self.normalizationLegendre_II(n, m + 2, cos_v)

        elif n == m and n == 0:
            return 1
        elif n == m and n == 1:
            return sqrt(3) * sin_theta
        elif n == 1 and m == 0:
            return sqrt(3) * cos_v
        elif n == m:
            pows = 1
            for i in range(2, n + 1):
                pows = pows * sqrt((2 * i) / (2 * i))
            return sin_theta ** n * pows
        else:
            # print("漏网之鱼", n, m)
            return 1


def test():
    modelPath = "E:\文档\大三课程\第三学期 - 物理大地测量学实习\数据\EGM08_360d"
    model = GravityModel(modelPath)
    m = model.modelData
    L = Legendre()
    # 测试勒让德级数
    saPath = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/L.txt"
    with open(saPath, "w") as F:
        for i in range(300):
            G = L.normalizationLegendre(int(m[i][0]), int(m[i][1]), cos(60 * pi / 180) )
            G2 = L.normalizationLegendre_II(int(m[i][0]), int(m[i][1]), cos(60 * pi / 180))
            # print("阶次", m[i][0], m[i][1], G, G2, G - G2)
            F.write("{}  {}  {}\n".format(m[i][0], m[i][1], G2))
