#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 重力测量数据处理工具包

@author: GanAH  2020/6/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


def observationDataCorrect(observationData, GZTranEnable, GZTable, tideTranEnable, tideTable):
    """
    重力观测改正
    :param observationData: 观测原始数据：n*2 list [observer_time,value]
    :param GZTranEnable: 格值改正接口
    :param GZTable: 格值改正表：n*3 list
    :return:
    """
    GZTranResult = observationData
    if GZTranEnable:  # 格值转换
        if len(GZTable) == 0:
            return {
                "code": 400,
                "result": None
            }
        else:  # 格值转换
            for i in range(len(observationData)):
                Ro = int(observationData[i][1] / 100) * 100
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
                # 计算转换值
                GZTranResult[i][1] = ao + a1 * (measureValue[i][1] - Ro)
    lastResult = GZTranResult
    if tideTranEnable:  # 潮汐改正
        if len(tideTable):
            return {"code": 402, "result": None}
        else:
            pass
            # 按照时间进行配比
            # TODO 按照时间

    return {"code": 1, "result": lastResult}
    # TODO 完善观测数据多层改正


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


def setReturnValue(list1, list2):
    return [
        list1[3], list1[4], list1[5], list1[6],
        list2[3], list2[4], list2[5], list2[6],
    ]


def queryTideTables(tideTable, year, month, day, find_UTCList):
    """
    查询潮汐表
    :param tideTable: 潮汐表
    :param year: 年
    :param month: 月
    :param day: 日
    :param find_UTCList: 待查询时间点列表
    :return: list [t1 gt1 t2 gt2]
    """
    result = []
    # judge
    for i in range(len(find_UTCList)):
        for k in range(len(tideTable)):
            if int(tideTable[k][2]) == day:
                timeMinute = float(tideTable[k][3]) * 60 + float(tideTable[k][4]) + float(tideTable[k][5]) / 60
                if timeMinute > find_UTCList[i]:
                    # lookback
                    timeMinuteBack = float(tideTable[k - 1][3]) * 60 + float(tideTable[k - 1][4]) + float(
                        tideTable[k - 1][5]) / 60
                    if timeMinuteBack < find_UTCList[i]:
                        print(find_UTCList[i], ":", timeMinuteBack, "-", tideTable[k - 1], timeMinute, "-",
                              tideTable[k])
                        result.append(setReturnValue(tideTable[k - 1], tideTable[k]))
                    elif timeMinuteBack == find_UTCList[i]:
                        print(find_UTCList[i], "*:", tideTable[k - 2], tideTable[k])
                        result.append(setReturnValue(tideTable[k - 2], tideTable[k]))

    print("\n\t======= 最终筛选出的数据========\n")
    view = False
    for i in range(len(result)):
        for k in range(len(result[0])):
            if k < 2 or k == 4 or k == 5:
                print(result[i][k], end=":")
            else:
                print(result[i][k], end="  ")
        if view:
            print()  # 换两行，print自带一行
        print()


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
