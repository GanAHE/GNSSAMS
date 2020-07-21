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
from numpy import sqrt, mat
from GNSS.timeSystem.timeChange import TimeSystemChange
from database.database import Database
import datetime


class ActionSPP(object):
    def __init__(self):
        pass

    def run(self):
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
        print(observationClass.observation.index, observationClass.observation.columns)
        # print(observationClass.observation.epoch[0],observationClass.observation["L1C"][observationClass.observation.epoch[0]])

        # 观测时刻UTC
        # intTimeFormat 实现如下转换：2019-10-28 08:33:15 --> [2019, 10, 28, 8, 33, 15]
        # intTimeFormat = lambda strT: list(map(int, ((strT.split())[0]).split("-") + ((strT.split())[1]).split(":")))
        # UTCList = intTimeFormat(str(observationClass.observation.epoch[0]))
        # # 将UTC转为JD
        # week,second = TimeSystemChange(UTCList[0], UTCList[1], UTCList[2], UTCList[3], UTCList[4], UTCList[5]).UTC2GPSTime()
        # JD = TimeSystemChange(week,second).GPSTime2JD()
        # print(UTCList,JD)
        # 读取导航点位
        navClass = readFile.read_navFile(path_NFile)
        # print(navClass.epoch)
        # 查看DataFrame的行列标志
        # print(navClass.navigation.index, navClass.navigation.columns)
        # 根据行键获取数据，key = ('2019-10-28 10:00:00', 'G10'),使用iloc可以根据行序获取，键值从观测文件找
        print(navClass.navigation.iloc[0].tolist())
        # getSatellitePositon(JD)
        oneDissList = navClass.navigation.loc[('2019-10-28 10:00:00', 'G10')].tolist()

        # 根据接收时间和伪距，计算信号发射时刻
        time_receiveSignal = "2019-10-28 08:33:15"
        satelliteName = "G10"
        waveBand = "C1C"
        waveDistance = observationClass.observation.loc[(time_receiveSignal, satelliteName)][waveBand]
        time = TimeSystemChange(2019, 10, 28, 8, 33, 15)
        week, tow = time.UTC2GPSTime()
        c = 2.99792458E8
        time_sendSignal = tow - waveDistance / c

        
        xyz = satelliteOrbetEtc.getSatellitePositon_II(time_sendSignal, oneDissList)
        print("卫星位置：", xyz)
        # 对卫星坐标进行地球自转改正
        # xyz = mat([[Database.earthRotationalAngularVelocity]]) * mat(xyz)
        # 测站近似坐标,一维list
        approx_position = observationClass.approx_position
        # 计算近似站星距离/伪距
        sum = 0
        for i in range(3):
            sum += (xyz[i][0] - approx_position[i]) * (xyz[i][0] - approx_position[i])
        approx_distance = sqrt(sum)
        print(approx_distance)
        # 对流层延迟/电离层延迟改正
    # 循环解算系数等完成
    # 平差求解

    # 改正
    # 精度评价： GDOP / PDOP / TDOP / HDOP / VDOP


ActionSPP().run()
