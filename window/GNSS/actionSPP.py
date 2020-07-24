#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 标准单点定位

@author: GanAH  2020/7/18.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import datetime
from GNSS.file import readFile
from GNSS.orbetEtc import satelliteOrbetEtc
from numpy import sqrt, mat, cos, sin, transpose, linalg, arctan, tan
from GNSS.timeSystem.timeChange import TimeSystemChange
from GNSS.correctionModel import tropCorrection, ionCorrection
from database.database import Database


class ActionSPP(object):
    def __init__(self):
        pass

    def getStationPosition(self, observationEpoch, waveBand, Sat, count_satellite, obsClass, navClass):

        # 卫星数量
        # count_satellite = len(PRN)
        # 光速 m/s
        c = 299792458
        # 地球自转角速度rad/s -RotationalAngularVelocity
        earth_RAV = 7.29211511467e-5
        # 测站近似坐标,一维list
        approxPosition = obsClass.approx_position

        # 判断与观测时间最近的导航电文时间
        delta = []
        navEpoch = navClass.navigation.epoch.index.values.tolist()
        for i in range(len(navEpoch)):
            delta.append((navEpoch[i][0] - observationEpoch).seconds)
        delta = list(map(abs, delta))
        num = 0
        navTime = ""
        for i in range(len(delta)):
            mindelta = min(delta)
            navTime = observationEpoch + datetime.timedelta(seconds=mindelta)
            if navTime.minute != 0 and navTime.second != 0:
                num = delta.index(mindelta)
                Sat.pop(num)
                delta.pop(num)
            else:
                break
        print(delta.pop(num))
        print(navTime)

        PRN = []
        for i in range(len(Sat)):
            PRN.append(Sat[i])
            if len(PRN) >= count_satellite:
                break
        print(PRN)

        # 构建系数矩阵
        B = []
        L = []
        for i in range(len(PRN)):
            satelliteName = PRN[i]
            # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
            # navEpochData = navClass.navigation.loc[(navClass.navigation.index.values[i][0], satelliteName)].tolist()
            navEpochData = navClass.navigation.loc[(navTime, satelliteName)].tolist()
            # 根据接收时间和伪距，计算信号发射时刻
            # time_receiveSignal = "2019-10-28 08:33:15"

            waveDistance = obsClass.observation.loc[(observationEpoch, satelliteName)][waveBand]

            # intTimeFormat 实现如下转换：2019-10-28 08:33:15 --> [2019, 10, 28, 8, 33, 15]
            intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
            UTCTimeList = intTimeFormat(str(observationEpoch))
            time_rec = TimeSystemChange(UTCTimeList[0], UTCTimeList[1], UTCTimeList[2], UTCTimeList[3], UTCTimeList[4],
                                        UTCTimeList[5])
            week, tow = time_rec.UTC2GPSTime()

            approxDistance = waveDistance
            temp = 0
            Vts = 0
            xyz = []
            while abs(temp - approxDistance) > 1e-6:
                temp = approxDistance
                teta_ts = approxDistance / c
                time_sendSignal = tow - teta_ts
                Vts, xyz = satelliteOrbetEtc.getSatellitePositon_II(time_sendSignal, navEpochData)
                # print(PRN[i]+"卫星位置：", xyz)
                # 对卫星坐标进行地球自转改正
                # xyz = mat([[cos(earth_RAV * teta_ts), sin(earth_RAV * teta_ts), 0],
                #            [-sin(earth_RAV * teta_ts), cos(earth_RAV * teta_ts), 0],
                #            [0, 0, 1]]) * mat(xyz)
                xyz = mat([[0, sin(earth_RAV * teta_ts), 0],
                             [-sin(earth_RAV * teta_ts), 0, 0],
                             [0, 0, 0]]) * mat(xyz) + mat(xyz)

                # xyz = xyz.tolist()
                # 计算近似站星距离/伪距
                sum = 0
                for k in range(3):
                    sum += (xyz[k, 0] - approxPosition[k]) * (xyz[k, 0] - approxPosition[k])
                approxDistance = sqrt(sum)
                print("迭代站星距：{}".format(approxDistance))

            # TODO 查找卫星仰角
            satelliteAngle = 15

            # 对流层延迟/电离层延迟改正
            if navClass.version[0] == 2:
                Vion = ionCorrection.klobuchar(satelliteAngle, UTCTimeList, approxPosition, xyz, navClass.alphalist,
                                               navClass.betalist)
            else:
                Vion = 0

            Vtrop = tropCorrection.tropospheric_delay(approxPosition[0], approxPosition[1], approxPosition[2],
                                                      satelliteAngle, UTCTimeList)
            B.append(
                [-(xyz[0, 0] - approxPosition[0]) / approxDistance,
                 -(xyz[1, 0] - approxPosition[1]) / approxDistance,
                 -(xyz[2, 0] - approxPosition[2]) / approxDistance,
                 -1])
            print("==+==", waveDistance - approxDistance)
            L.append([waveDistance - c * Vts + Vion + Vtrop - approxDistance])

        # 循环解算系数等完成
        # 平差求解
        matrix_B = mat(B)
        matrix_L = mat(L)
        print("--matrix_B:\n", matrix_B)
        print("--matrix_L:\n", matrix_L)
        Q = linalg.inv(transpose(matrix_B) * matrix_B)
        matrix_x = Q * (transpose(matrix_B) * matrix_L)
        matrix_v = matrix_B * matrix_x - matrix_L
        print("--matrix_x:\n", matrix_x)
        print("--matrix_v:\n", matrix_v)
        sigma_o = sqrt((transpose(matrix_v) * matrix_v)[0, 0] / (count_satellite - 4))
        print("中误差：{} mm".format(sigma_o * 1e3))
        # D = sigma_o * sigma_o * Q
        # 改正
        stationPosition = [approxPosition[0] + matrix_x[0, 0], approxPosition[1] + matrix_x[1, 0],
                           approxPosition[2] + matrix_x[2, 0]]
        print("近似坐标：", approxPosition, "\n最后坐标：", stationPosition)
        # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP
        # 三维点位精度衰减因子
        PDOP = sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
        # 时间精度衰减因子
        TDOP = sqrt(Q[3, 3])
        # 几何精度衰减因子
        GDOP = sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])

        print("GDOP / PDOP / TDOP ", GDOP, PDOP, TDOP)


def actionReadFile():
    try:
        # 从数据库获取文件路径
        # path_OFile = Database.oFilePathList[0]
        # path_NFile = Database.nFilePathList[0]
        path_OFile = r"E:\CodePrograme\Python\EMACS\workspace\GNSS\D068305A.19O"
        path_NFile = r"E:\CodePrograme\Python\EMACS\workspace\GNSS\D068305A.19N"

        # 读取观测文件并提取对应数据
        obsClass = readFile.read_obsFile(path_OFile)
        obsEpoch = obsClass.observation.epoch.index.values.tolist()
        # 选定一个观测时间
        obsTime = obsEpoch[0][0]
        # print(obsEpoch,type(obsClass.observation.epoch))
        # sv =obsClass.observation.loc[(obsTime,obsEpoch[0][1])]
        Sat = []
        count_satellite = 6
        for k in range(len(obsEpoch)):
            if obsTime == obsEpoch[k][0]:
                if (obsEpoch[k][1])[0] == "G":
                    Sat.append(obsEpoch[k][1])
                # elif (obsEpoch[k][1])[0] == "R":
                #     PR
            # if len(PRN) >= count_satellite:
            #     break
        print(Sat)

        # 读取导航电文
        navClass = readFile.read_navFile(path_NFile)

        ActionSPP().getStationPosition(obsTime, "C1C", Sat, count_satellite, obsClass, navClass)
    except Exception as e:
        print(e.__str__())


# actionReadFile()
