#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 坐标转换类

@author: GanAH  2020/2/10.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


class CoordinationTran():

    def __init__(self, *args):
        self.XYZ = args[0]
        self.BLH = args[1]
        self.NEH = args[2]

    def BLH_to_XYZ(self, BLH):
        pass

    def XYZ_to_BLH(self, XYZ):
        pass

    def XYZ_to_NEH(self, XYZ):
        pass

    def NEH_to_XYZ(self, NEH):
        pass

    def BLH_to_NEH(self, BLH):
        """
        BLH 转 NEH
        <p> 中转
        :param BLH:
        :return:
        """
        return self.XYZ_to_NEH(self.BLH_to_XYZ(BLH))

    def NEH_to_BLH(self, NEH):
        self.XYZ_to_BLH(self.NEH_to_XYZ(NEH))
