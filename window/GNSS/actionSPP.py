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
from database.database import Database
import datetime


class ActionSPP(object):
    def __init__(self):
        pass

    def run(self):
        # 选定的卫星PRN
        PRN = ["G10", "G12", "G14", "G15", "G20"]
        observationEpoch = "2019-10-28 08:33:15"
        # 卫星数量
        count_satellite = len(PRN)
        # 光速 m/s
        light_speed = 299792458
        # 从数据库获取文件路径
        # path_OFile = Database.oFilePath
        # path_NFile = Database.nFilePath
        # path_OFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19o"
        # path_NFile = r"E:\\CodePrograme\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19n"
        path_OFile = r"d:\\CodeProgram\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19o"
        path_NFile = r"d:\\CodeProgram\\Python\\EMACS\\workspace\\GNSS\\GP008301I.19n"
        # 读取观测文件并提取对应数据
        observationClass = readFile.read_obsFile(path_OFile)
        # 查看键值
        print("观测文件", observationClass.observation.index, observationClass.observation.columns)
        # print(observationClass.observation.epoch[0],observationClass.observation["L1C"][observationClass.observation.epoch[0]])

        # 观测时刻UTC
        # intTimeFormat 实现如下转换：2019-10-28 08:33:15 --> [2019, 10, 28, 8, 33, 15]
        # intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
        # UTCList = intTimeFormat(str(observationClass.observation.epoch[0]))
        # 读取导航电文
        navClass = readFile.read_navFile(path_NFile)
        # 查看DataFrame的行列标志
        # print(navClass.navigation.index, navClass.navigation.columns)
        # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
        print(navClass.navigation.iloc[0].tolist())
        # getSatellitePositon(JD)
        oneDissList = navClass.navigation.loc[('2019-10-28 10:00:00', 'G10')].tolist()

        # 测站近似坐标,一维list
        approx_position = observationClass.approx_position
        satellitesCoordinateXYZ = []
        approxDistanceList = []
        B = []
        L = []
        for i in range(count_satellite):
            # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
            oneDissList = navClass.navigation.loc[('2019-10-28 10:00:00', 'G10')].tolist()

            # 根据接收时间和伪距，计算信号发射时刻
            # time_receiveSignal = "2019-10-28 08:33:15"
            satelliteName = PRN[i]
            waveBand = "C1C"
            waveDistance = observationClass.observation.loc[(observationEpoch, satelliteName)][waveBand]
            time = TimeSystemChange(2019, 10, 28, 8, 33, 15)
            week, tow = time.UTC2GPSTime()

            approx_distance = waveDistance
            temp = 0
            while (temp - approx_distance) > 10e8:
                temp = approx_distance
                teta_ts = approx_distance / light_speed
                time_sendSignal = tow - teta_ts
                Vts, xyz = satelliteOrbetEtc.getSatellitePositon_II(time_sendSignal, oneDissList)
                # print(PRN[i]+"卫星位置：", xyz)
                # 对卫星坐标进行地球自转改正
                xyz = mat([[cos(Database.earth_RAV * teta_ts), sin(Database.earth_RAV * teta_ts), 0],
                           [-sin(Database.earth_RAV * teta_ts), cos(Database.earth_RAV * teta_ts), 0],
                           [0, 0, 1]]) * mat(xyz)
                xyz = xyz.tolist()
                # 计算近似站星距离/伪距
                sum = 0
                for i in range(3):
                    sum += (xyz[i][0] - approx_position[i]) * (xyz[i][0] - approx_position[i])
                approx_distance = sqrt(sum)
            print(approx_distance)
            # 对流层延迟/电离层延迟改正
            Vion = 0
            Vtrop = 0
            # 构建系数矩阵
            B.append(
                [-(xyz[0][0] - approx_position[0]) / approx_distance,
                 (xyz[1][0] - approx_position[1]) / approx_distance,
                 -(xyz[2][0] - approx_position[2]) / approx_distance,
                 -1])
            L.append([waveDistance - light_speed * Vts + Vion + Vtrop - approx_distance])

        # 循环解算系数等完成
        # 平差求解
        matrix_B = mat(B)
        matrix_L = mat(L)
        print("matrix_B:", matrix_B)
        print("matrix_L:", matrix_L)
        Q = linalg.inv(transpose(matrix_B) * matrix_B)
        matrix_x = Q * transpose(B) * matrix_L
        matrix_v = matrix_B * matrix_x - matrix_L
        sigma_o = sqrt((transpose(matrix_v) * matrix_v).tolist()[0][0] / (count_satellite - 4))
        D = sigma_o * sigma_o * Q
        # 改正
        x = matrix_x.tolist()
        stationPosition = [approx_position[0] + x[0][0], approx_position[1] + x[1][0], approx_position[2] + x[2][0], ]
        print("近似坐标：", approx_position, "\n最后坐标：", stationPosition)
        # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP
        Q = Q.tolist()
        # 三维点位精度衰减因子
        PDOP = sqrt(Q[0][0] + Q[1][1] + Q[2][2])
        # 时间精度衰减因子
        TDOP = sqrt(Q[3][3])
        # 几何精度衰减因子
        GDOP = sqrt(Q[0][0] + Q[1][1] + Q[2][2] + Q[3][3])

        print("GDOP / PDOP / TDOP ",GDOP,PDOP,TDOP)


ActionSPP().run()
