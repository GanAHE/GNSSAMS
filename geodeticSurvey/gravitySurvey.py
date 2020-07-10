#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 重力测量数据处理工具包

@author: GanAH  2020/6/28.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import csv
from math import sin, cos, pi


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
                GZTranResult[i][1] = ao + a1 * (observationData[i][1] - Ro)
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


def normalGravity(fia, type=None, H=None):
    """
    计算正常重力值
    :param fia: 大地纬度
    :param type: 模型公式
    :param H: 大地水准面上高度
    :return: cm/s^2 or Gal
    """
    fia = fia * pi / 180
    if type == "hemote":
        yo = 978030.0 * (1 + 0.005302 * sin(fia) * sin(fia) - 0.000007 * sin(2 * fia) * sin(2 * fia))
    elif type == "casni":
        yo = 978049.0 * (1 + 0.005288 * sin(fia) * sin(fia) - 0.0000059 * sin(2 * fia) * sin(2 * fia))
    else:
        yo = 978032.0 * (1 + 0.005302 * sin(fia) * sin(fia) - 0.0000058 * sin(2 * fia) * sin(2 * fia))

    if H is None:  # 水准面上正常重力
        return yo
    else:  # 地面H出正常重力
        return yo - 0.3086 * H


def gridCacu():
    Data = []
    csvPath = "E:/文档/大三课程/第三学期 - 物理大地测量学实习/数据/Grid.csv"
    with open(csvPath, "r") as F:
        reader = csv.reader(F)
        count = 1
        for row in reader:
            if count == 1:
                count = 2
                Data.append(row)
            else:
                lineData = list(map(float, row[1:5]))
                print("重力异常:", lineData[3] - normalGravity(lineData[1], H=lineData[2]) - 0.1116 * lineData[2])
                row[5] = lineData[3] - normalGravity(lineData[1], H=lineData[2] - 0.1116 * lineData[2])
                Data.append(row)
    F.close()
    for i in range(len(Data)):
        print(Data[i][5])


def NetCacu():
    """
    基线联测
    :return:
    """
    Data = [[2, 114.3569444, 30.53138889, 41, 979349.183300],
            [4, 114.353121, 30.532709, 37, 979349.738555],
            [5, 114.352441, 30.532003, 34, 979350.709845],
            [3, 114.353763, 30.531887, 39, 979350.657243],
            [6, 114.353044, 30.529602, 37, 979351.344532],
            [7, 114.35465, 30.529754, 41, 979351.081257],
            [8, 114.354571, 30.528564, 40, 979349.974796]]

    re = []
    for i in range(len(Data)):
        print("基线联测重力异常:", Data[i][4] - normalGravity(Data[i][2], H=Data[i][3]) - 0.1116 * Data[i][3])
        re.append([Data[i][4] - normalGravity(Data[i][2], H=Data[i][3]),
                   Data[i][4] - normalGravity(Data[i][2], H=Data[i][3]) - 0.1116 * Data[i][3]])
    # 完成
    print("===========")
    for i in range(len(re)):
        print(re[i])

# NetCacu()
# gridCacu()
