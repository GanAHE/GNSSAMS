#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: DengGZC  2020/7/23.
@version 1.0.
@contact: dgzc159@163.com
"""

from GNSS.file import readFile
from GNSS.correctionModel import tropCorrection, ionCorrection
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D

def coefficients(x, m, seconds):   # 计算L系数
    l = 1
    for i in range(len(seconds)):
        if seconds[i] != m:
            l_delta = (x - seconds[i]) / (m - seconds[i])
            l *= l_delta
            # print(l_delta)
        else:
            l *= 1
    # print(l)
    return l

def readfile():
    path_sp3FilePast = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20770.sp3"
    path_sp3FileNow = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20771.sp3"
    path_sp3FileFuture = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20772.sp3"
    # path_sp3File = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20771.sp3"
    path_oFile = r"D:\CodeProgram\Python\EMACS\workspace\GNSS\GP008301I.19o"

    sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
    sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
    sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)
    # sp3Class = readFile.read_sp3File(path_sp3File)
    obsClass = readFile.read_obsFile(path_oFile)

    sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
    sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
    sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()
    # sp3Epoch = sp3Class.ephemeris.index.values.tolist()
    obsEpoch = obsClass.observation.index.values.tolist()

    intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))

    obsTime = obsEpoch[0][0]
    print(obsTime)
    obsTimeList = intTimeFormat(str(obsTime))
    time = obsTimeList[3] + obsTimeList[4] / 60 + obsTimeList[5] / 3600
    print(time)
    approx_position = obsClass.approx_position

    Sat = []
    count_satellite = 6
    for k in range(len(obsEpoch)):
        if obsTime == obsEpoch[k][0]:
            if (obsEpoch[k][1])[0] == "G":
                Sat.append(obsEpoch[k][1])
        if len(Sat) == count_satellite:
            break
    print(Sat)

    x = []
    y = []
    z = []
    satellite_x = []
    satellite_y = []
    satellite_z = []
    B = []
    L = []
    for j in range(len(Sat)):
        print(Sat[j])
        timePastList = []
        timeNowList = []
        timeFutureList = []
        epochPast = []
        epochNow = []
        epochFuture = []
        for i in range(len(sp3PastEpoch)):
            if sp3PastEpoch[i][1] == Sat[j]:
                timePastList.append(intTimeFormat(str(sp3PastEpoch[i][0])))
                epochPast.append(sp3PastEpoch[i][0])

        for i in range(len(sp3NowEpoch)):
            if sp3NowEpoch[i][1] == Sat[j]:
                timeNowList.append(intTimeFormat(str(sp3NowEpoch[i][0])))
                epochNow.append(sp3NowEpoch[i][0])

        for i in range(len(sp3FutureEpoch)):
            if sp3FutureEpoch[i][1] == Sat[j]:
                timeFutureList.append(intTimeFormat(str(sp3FutureEpoch[i][0])))
                epochFuture.append(sp3FutureEpoch[i][0])
        # print(epochPast)

        timePastSeconds = []
        timeNowSeconds = []
        timeFutureSeconds = []
        dx = []
        dy = []
        dz = []
        for i in range(len(timePastList)):
            timePastSeconds.append(timePastList[i][3] + timePastList[i][4] / 60 + timePastList[i][5] / 3600)
            dx.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"])
            dy.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"])
            dz.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"])

        for i in range(len(timeNowList)):
            timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
            dx.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"])
            dy.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"])
            dz.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"])

        for i in range(len(timeFutureList)):
            timeFutureSeconds.append(timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
            dx.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"])
            dy.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"])
            dz.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"])

        x.append(dx)
        y.append(dy)
        z.append(dz)

        timeSeconds = []
        for i in range(len(timePastSeconds)):
            timeSeconds.append(timePastSeconds[i] - 24)

        for i in range(len(timeNowSeconds)):
            timeSeconds.append(timeNowSeconds[i])

        for i in range(len(timeFutureSeconds)):
            timeSeconds.append(timeFutureSeconds[i] + 24)

        px = 0
        py = 0
        pz = 0
        for m in range(len(timeSeconds)):
            px_delta = x[j][m] * coefficients(time, timeSeconds[m], timeSeconds)
            px += px_delta
            py_delta = y[j][m] * coefficients(time, timeSeconds[m], timeSeconds)
            py += py_delta
            pz_delta = z[j][m] * coefficients(time, timeSeconds[m], timeSeconds)
            pz += pz_delta
        satellite_x.append(px)
        satellite_y.append(py)
        satellite_z.append(pz)

        satelliteName = Sat[j]
        waveBand = "C1C"
        waveDistance = obsClass.observation.loc[(obsTime, satelliteName)][waveBand]

        approxDistance = np.sqrt((satellite_x[j] - approx_position[0]) ** 2 + (satellite_y[j] - approx_position[1]) ** 2 + (satellite_z[j] - approx_position[2]) ** 2)

        # TODO 查找卫星仰角
        satelliteAngle = 15

        # 对流层延迟/电离层延迟改正
        Vion = 0

        Vtrop = tropCorrection.tropospheric_delay(approx_position[0], approx_position[1], approx_position[2],
                                                  satelliteAngle, obsTimeList)

        B.append(
            [-(satellite_x[j] - approx_position[0]) / approxDistance,
             -(satellite_y[j] - approx_position[1]) / approxDistance,
             -(satellite_z[j] - approx_position[2]) / approxDistance,
             -1])
        L.append([waveDistance + Vion + Vtrop - approxDistance])

    # 平差求解
    matrix_B = np.mat(B)
    matrix_L = np.mat(L)
    Q = np.linalg.inv(np.transpose(matrix_B) * matrix_B)
    matrix_x = Q * (np.transpose(matrix_B) * matrix_L)
    matrix_v = matrix_B * matrix_x - matrix_L
    sigma_o = np.sqrt((np.transpose(matrix_v) * matrix_v)[0, 0] / (count_satellite - 4))
    stationPosition = [approx_position[0] + matrix_x[0, 0], approx_position[1] + matrix_x[1, 0], approx_position[2] + matrix_x[2, 0]]

    print(Vtrop)
    print(waveDistance)
    print(approxDistance)
    print(matrix_B)
    print(matrix_L)
    print(matrix_x)
    print(stationPosition)

    # print(satellite_x)
    # print(satellite_y)
    # print(satellite_z)

# readfile()

def satelliteOrbits():
    path_sp3FilePast = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20770.sp3"
    path_sp3FileNow = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20771.sp3"
    path_sp3FileFuture = r"d:\CodeProgram\Python\EMACS\workspace\GNSS\igs20772.sp3"

    sp3PastClass = readFile.read_sp3File(path_sp3FilePast)
    sp3NowClass = readFile.read_sp3File(path_sp3FileNow)
    sp3FutureClass = readFile.read_sp3File(path_sp3FileFuture)

    sp3PastEpoch = sp3PastClass.ephemeris.index.values.tolist()
    sp3NowEpoch = sp3NowClass.ephemeris.index.values.tolist()
    sp3FutureEpoch = sp3FutureClass.ephemeris.index.values.tolist()


    Sat = []
    sp3NowTime = sp3NowEpoch[0][0]
    for k in range(len(sp3NowEpoch)):
        if sp3NowTime == sp3NowEpoch[k][0]:
            Sat.append(sp3NowEpoch[k][1])
    print(Sat)

    intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))

    x = []
    y = []
    z = []
    timeSeconds = []
    for j in range(len(Sat)):
        print(Sat[j])
        timePastList = []
        timeNowList = []
        timeFutureList = []
        epochPast = []
        epochNow = []
        epochFuture = []
        for i in range(len(sp3PastEpoch)):
            if sp3PastEpoch[i][1] == Sat[j]:
                timePastList.append(intTimeFormat(str(sp3PastEpoch[i][0])))
                epochPast.append(sp3PastEpoch[i][0])

        for i in range(len(sp3NowEpoch)):
            if sp3NowEpoch[i][1] == Sat[j]:
                timeNowList.append(intTimeFormat(str(sp3NowEpoch[i][0])))
                epochNow.append(sp3NowEpoch[i][0])

        for i in range(len(sp3FutureEpoch)):
            if sp3FutureEpoch[i][1] == Sat[j]:
                timeFutureList.append(intTimeFormat(str(sp3FutureEpoch[i][0])))
                epochFuture.append(sp3FutureEpoch[i][0])
        # print(epochPast)

        timePastSeconds = []
        timeNowSeconds = []
        timeFutureSeconds = []
        dx = []
        dy = []
        dz = []
        for i in range(len(timePastList)):
            timePastSeconds.append(timePastList[i][3] + timePastList[i][4] / 60 + timePastList[i][5] / 3600)
            dx.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["X"])
            dy.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Y"])
            dz.append(sp3PastClass.ephemeris.loc[(epochPast[i], Sat[j])]["Z"])

        for i in range(len(timeNowList)):
            timeNowSeconds.append(timeNowList[i][3] + timeNowList[i][4] / 60 + timeNowList[i][5] / 3600)
            dx.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["X"])
            dy.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Y"])
            dz.append(sp3NowClass.ephemeris.loc[(epochNow[i], Sat[j])]["Z"])

        for i in range(len(timeFutureList)):
            timeFutureSeconds.append(timeFutureList[i][3] + timeFutureList[i][4] / 60 + timeFutureList[i][5] / 3600)
            dx.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["X"])
            dy.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Y"])
            dz.append(sp3FutureClass.ephemeris.loc[(epochFuture[i], Sat[j])]["Z"])

        x.append(dx)
        y.append(dy)
        z.append(dz)
        # print(dx)
        # print(x)

        timeSeconds.clear()
        for i in range(len(timePastSeconds)):
            timeSeconds.append(timePastSeconds[i] - 24)

        for i in range(len(timeNowSeconds)):
            timeSeconds.append(timeNowSeconds[i])

        for i in range(len(timeFutureSeconds)):
            timeSeconds.append(timeFutureSeconds[i] + 24)

        # print(timeSeconds)
    # print(x[2][5])
    # # 生成画布
    # fig = plt.figure()

    # 打开交互模式
    plt.ion()

    # # 清除原有图像
    # fig.clf()

    time = np.linspace(0, 24, 24 * 5, endpoint=True)

    for j in range(len(Sat)):
        print(Sat[j])
        satellite_x = []
        satellite_y = []
        satellite_z = []

        # 生成画布
        fig = plt.figure()

        # 清除原有图像
        fig.clf()

        for i in range(len(time)):
            px = 0
            py = 0
            pz = 0
            for m in range(len(timeSeconds)):
                px_delta = x[j][m] * coefficients(time[i], timeSeconds[m], timeSeconds)
                px += px_delta
                py_delta = y[j][m] * coefficients(time[i], timeSeconds[m], timeSeconds)
                py += py_delta
                pz_delta = z[j][m] * coefficients(time[i], timeSeconds[m], timeSeconds)
                pz += pz_delta
            satellite_x.append(px)
            satellite_y.append(py)
            satellite_z.append(pz)

        # 生成画布
        ax = fig.gca(projection='3d')
        # 画三维散点图
        for i in range(len(time)):
            ax.scatter(satellite_x[i], satellite_y[i], satellite_z[i], c = "r", marker = ".")

        # 设置坐标轴范围
        ax.set_xlim(-30000, 30000)
        ax.set_ylim(-30000, 30000)
        ax.set_zlim(-30000, 30000)

        plt.pause(0.2)

    # 关闭交互模式
    plt.ioff()

    # 图形显示
    plt.show()
    return

        # print(satellite_x)

    # print(x[2][5])





satelliteOrbits()









# def read():
#     path_sp3File = r"D:\CodeProgram\Python\EMACS\workspace\GNSS\igs20775.sp3"
#
#     sp3Class = readFile.read_sp3File(path_sp3File)
#     sp3Epoch = sp3Class.ephemeris.index.values.tolist()
#
#     sat = sp3Epoch[1][1]  # 选择一颗卫星
#
#     timeList = []
#     epoch = []
#     for i in range(len(sp3Epoch)):
#         if sp3Epoch[i][1] == sat:
#             intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
#             timeList.append(intTimeFormat(str(sp3Epoch[i][0])))
#             epoch.append(sp3Epoch[i][0])
#
#     timeSeconds = []
#     x = []
#     y = []
#     z = []
#     for i in range(len(timeList)):
#         timeSeconds.append(timeList[i][3] + timeList[i][4] / 60 + timeList[i][5] / 3600)
#         x.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["X"])
#         y.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["Y"])
#         z.append(sp3Class.ephemeris.loc[(epoch[i], sat)]["Z"])
#     print(timeSeconds)
#
#     time = 20.3  # 选择一个观测时间
#     px = 0
#     py = 0
#     pz = 0
#     for m in range(len(timeSeconds)):
#         px_delta = x[m] * coefficients(time, timeSeconds[m], timeSeconds)
#         px += px_delta
#         py_delta = y[m] * coefficients(time, timeSeconds[m], timeSeconds)
#         py += py_delta
#         pz_delta = z[m] * coefficients(time, timeSeconds[m], timeSeconds)
#         pz += pz_delta
#     print(px)
#     print(py)
#     print(pz)
#
# read()
