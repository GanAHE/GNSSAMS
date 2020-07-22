#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 标准单点定位

@author: GanAH  2020/7/18.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from GNSS.file import readFile
from GNSS.orbetEtc import satelliteOrbetEtc
from numpy import sqrt, mat, cos, sin, transpose, linalg
from GNSS.timeSystem.timeChange import TimeSystemChange
from GNSS.correctionModel import tropCorrection


class ActionSPP(object):
    def __init__(self):
        pass

    def run(self, observationEpoch, waveBand, PRN, observationClass, navClass):

        # 卫星数量
        count_satellite = len(PRN)
        # 光速 m/s
        c = 299792458
        # 地球自转角速度rad/s -RotationalAngularVelocity
        earth_RAV = 7.29211511467e-5

        # 查看键值
        # print("观测文件", observationClass.observation.index, observationClass.observation.columns)
        # 查看DataFrame的行列标志
        # print(navClass.navigation.index, navClass.navigation.columns)

        # 测站近似坐标,一维list
        approx_position = observationClass.approx_position

        B = []
        L = []
        for i in range(count_satellite):
            satelliteName = PRN[i]
            # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
            navEpochData = navClass.navigation.loc[(navClass.navigation.index.values[i][0], satelliteName)].tolist()

            # 根据接收时间和伪距，计算信号发射时刻
            # time_receiveSignal = "2019-10-28 08:33:15"

            waveDistance = observationClass.observation.loc[(observationEpoch, satelliteName)][waveBand]

            approx_distance = waveDistance
            # intTimeFormat 实现如下转换：2019-10-28 08:33:15 --> [2019, 10, 28, 8, 33, 15]
            intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
            UTCTimeList = intTimeFormat(str(observationEpoch))
            time_rec = TimeSystemChange(UTCTimeList[0], UTCTimeList[1], UTCTimeList[2], UTCTimeList[3], UTCTimeList[4], UTCTimeList[5])
            week, tow = time_rec.UTC2GPSTime()
            temp = 0
            Vts = 0
            xyz = []
            while abs(temp - approx_distance) > 1e-6:
                temp = approx_distance
                teta_ts = approx_distance / c
                time_sendSignal = tow - teta_ts
                Vts, xyz = satelliteOrbetEtc.getSatellitePositon_II(time_sendSignal, navEpochData)
                # print(PRN[i]+"卫星位置：", xyz)
                # 对卫星坐标进行地球自转改正
                xyz = mat([[cos(earth_RAV * teta_ts), sin(earth_RAV * teta_ts), 0],
                           [-sin(earth_RAV * teta_ts), cos(earth_RAV * teta_ts), 0],
                           [0, 0, 1]]) * mat(xyz)
                # xyz = xyz.tolist()
                # 计算近似站星距离/伪距
                sum = 0
                for k in range(3):
                    sum += (xyz[k, 0] - approx_position[k]) * (xyz[k, 0] - approx_position[k])
                approx_distance = sqrt(sum)
                # print("迭代站星距：{}".format(approx_distance))

            # 对流层延迟/电离层延迟改正
            Vion = 0
            # TODO 查找卫星仰角
            staelliteAngle = 15
            Vtrop = tropCorrection.tropospheric_delay(approx_position[0], approx_position[1],approx_position[2],staelliteAngle,UTCTimeList)
            # 构建系数矩阵
            B.append(
                [-(xyz[0, 0] - approx_position[0]) / approx_distance,
                 -(xyz[1, 0] - approx_position[1]) / approx_distance,
                 -(xyz[2, 0] - approx_position[2]) / approx_distance,
                 -1])
            L.append([waveDistance - c * Vts + Vion + Vtrop - approx_distance])

        # 循环解算系数等完成
        # 平差求解
        matrix_B = mat(B)
        matrix_L = mat(L)
        print("matrix_B:", matrix_B)
        print("matrix_L:", matrix_L)
        Q = linalg.inv(transpose(matrix_B) * matrix_B)
        matrix_x = Q * (transpose(matrix_B) * matrix_L)
        matrix_v = matrix_B * matrix_x - matrix_L
        sigma_o = sqrt((transpose(matrix_v) * matrix_v)[0, 0] / (count_satellite - 4))
        print("中误差：{} mm".format(sigma_o * 1e3))
        # D = sigma_o * sigma_o * Q
        # 改正
        stationPosition = [approx_position[0] + matrix_x[0, 0], approx_position[1] + matrix_x[1, 0],
                           approx_position[2] + matrix_x[2, 0]]
        print("近似坐标：", approx_position, "\n最后坐标：", stationPosition)
        # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP
        Q = Q.tolist()
        # 三维点位精度衰减因子
        PDOP = sqrt(Q[0][0] + Q[1][1] + Q[2][2])
        # 时间精度衰减因子
        TDOP = sqrt(Q[3][3])
        # 几何精度衰减因子
        GDOP = sqrt(Q[0][0] + Q[1][1] + Q[2][2] + Q[3][3])

        print("GDOP / PDOP / TDOP ", GDOP, PDOP, TDOP)


def actionReadFile():
    # 从数据库获取文件路径
    # path_OFile = Database.oFilePath
    # path_NFile = Database.nFilePath
    path_OFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19o"
    path_NFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19n"
    # path_OFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\D068305A.19O"
    # path_NFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\D068305A.19N"
    # path_OFile = r"d:\\CodeProgram\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19o"
    # path_NFile = r"d:\\CodeProgram\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19n"

    # 读取观测文件并提取对应数据
    observationClass = readFile.read_obsFile(path_OFile)
    obsEpoch = observationClass.observation.epoch.index.values.tolist()
    # 选定一个观测时间
    obsTime = \
        obsEpoch[0][0]
    # print(obsEpoch,type(observationClass.observation.epoch))
    # sv =observationClass.observation.loc[(obsTime,obsEpoch[0][1])]
    PRN = []
    count_satellite = 5
    for k in range(len(obsEpoch)):
        if k >= count_satellite:
            break
        if obsTime == obsEpoch[k][0]:
            if (obsEpoch[k][1])[0] == "G":
                PRN.append(obsEpoch[k][1])
            # elif (obsEpoch[k][1])[0] == "R":
            #     PR
    print(PRN)

    # 读取导航电文
    navClass = readFile.read_navFile(path_NFile)

    navEpoch = navClass.epoch
    actionSPP = ActionSPP().run(obsTime, "C1C", PRN, observationClass, navClass)


# ActionSPP().run()
actionReadFile()
