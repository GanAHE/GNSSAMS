#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 重力测量数据处理工具包

@author: GanAH  2020/6/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


def GZTran(GZTable, measureValue):
    """
    格值转换
    :param GZTable: 格值表，根据仪器型号获取，数据形式为 N*3 二维数据格式
    :param measureValue: 测量数据值
    :return:
    """
    GZTran = []
    for i in range(len(measureValue)):
        Ro = int(measureValue[i] / 100) * 100
        # 格值比对
        ao = 0
        a1 = 0
        for k in range(len(GZTable)):
            if Ro == GZTable[k][0]:
                ao = GZTable[k][1]
                a1 = GZTable[k][2]
                break
            if k == len(GZTable) - 1:
                print("未能在格值表查到对应值")
        # 计算
        GZTran.append(ao + a1 * (measureValue[i] - Ro))
    return GZTran


GZTable = [[2800, 2847.38, 1.01842],
           [2900, 2949.22, 1.01856]]

measureValue = [
    2900.567,
    2898.406,
    2894.159,
    2889.785,
    2885.453,
    2889.753,
    2894.112,
    2898.344,
    2900.526
]
GZTrn = GZTran(GZTable, measureValue)
for t in range(len(GZTrn)):
    print("最终结果", GZTrn[t])
