#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/7/23.
@version 1.0.
@contact: dgzc159@163.com
"""

from GNSS.file import readFile

def coefficients(x, j, k, seconds):   # 计算L系数
    l = 1
    for i in range(k):
        if seconds[i] != j:
            l_delta = (x - seconds[i]) / (j - seconds[i])
            l *= l_delta
            # print(l_delta)
        else:
            l *= 1
    return l
    # print(l)


def readfile():
    path_sp3File = r"D:\CodeProgram\Python\EMACS\workspace\GNSS\igs20775.sp3"

    sp3Class = readFile.read_sp3File(path_sp3File)
    sp3Epoch = sp3Class.ephemeris.index.values.tolist()

    sat = sp3Epoch[1][1]   #选择一颗卫星

    timeList = []
    epoch = []
    for i in range(len(sp3Epoch)):
        if sp3Epoch[i][1] == sat:
            intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
            timeList.append(intTimeFormat(str(sp3Epoch[i][0])))
            epoch.append(sp3Epoch[i][0])

    timeSeconds = []
    x = []
    y = []
    z = []
    for i in range(len(timeList)):
        timeSeconds.append(timeList[i][3] + timeList[i][4] / 60 + timeList[i][5] / 3600)
        x.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["X"])
        y.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["Y"])
        z.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["Z"])
    print(timeSeconds)

    time = 2.0   #选择一个观测时间
    px = 0
    py = 0
    pz = 0
    for m in range(len(timeSeconds)):
        px_delta = x[m] * coefficients(time, timeSeconds[m], len(timeSeconds), timeSeconds)
        px += px_delta
        py_delta = y[m] * coefficients(time, timeSeconds[m], len(timeSeconds), timeSeconds)
        py += py_delta
        pz_delta = z[m] * coefficients(time, timeSeconds[m], len(timeSeconds), timeSeconds)
        pz += pz_delta
    print(px)
    print(py)
    print(pz)

readfile()

