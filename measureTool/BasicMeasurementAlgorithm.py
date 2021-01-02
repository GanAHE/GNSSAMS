#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 计算坐标方位角

@author: GanAH  2020/4/9.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

import math


class BasicMeasurementAlgorithm(object):

    def calc_angle(self, Xa, Ya, Xb, Yb):
        """
        两点坐标方位角
        :param Xa:
        :param Ya:
        :param Xb:
        :param Yb:
        :return: 度
        """

        angle = 0
        teta_X = Xb - Xa
        teta_Y = Yb - Ya
        # 判别
        if teta_X == 0:
            if teta_Y > 0:
                angle = 90
            elif teta_Y < 0:
                angle = 270
            else:
                pass
        elif teta_X > 0:  # Xb > Xa
            if teta_Y > 0:
                angle = math.atan(teta_Y / teta_X) * 180 / math.pi
            elif teta_Y == 0:
                angle = 0
            else:
                angle = 360 + math.atan(teta_Y / teta_X) * 180 / math.pi
        else:
            if teta_Y == 0:
                angle = 180
            else:
                angle = 180 + math.atan(teta_Y / teta_X) * 180 / math.pi

        return angle

    # 由一点和距离计算另一点的坐标
    def coorForwarkCaclulator(self, gridBearingAngle, distance, sourceX, sourceY):
        """
        坐标正算
        :param gridBearing: 坐标方位角--单位：°
        :param distance: 两点距离
        :param sourceX: 已知坐标X
        :param sourceY: 已知坐标Y
        :return: None
        """
        return sourceX + distance * math.cos(gridBearingAngle), sourceY + distance * math.sin(gridBearingAngle)

    def coorBackCaclulator(self, listTwoCoor):
        """
        批量坐标反算
        :param listTwoCoor: 二维坐标对 a,b点--[[Xa,Ya,Xb,Yb],..]
        :return: 二维坐标对--[[ab坐标方位角：gridBearingAngle,ab点距离：distance],..]
        """

        resultList = []
        for i in range(len(listTwoCoor)):
            teta_X = listTwoCoor[i][2] - listTwoCoor[i][0]
            teta_Y = listTwoCoor[i][3] - listTwoCoor[i][1]
            gridBearingAngle = self.calc_angle(listTwoCoor[i][0], listTwoCoor[i][1], listTwoCoor[i][2],
                                               listTwoCoor[i][3])
            distance = math.sqrt(teta_X * teta_X + teta_Y * teta_Y)
            resultList.append([gridBearingAngle, distance])
        return resultList


