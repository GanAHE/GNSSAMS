#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 相对稳定点组测定

@author: GanAH  2020/4/24.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math

import numpy as np


class StablePointGroup(object):

    def __init__(self, strMeasureList_I, strMeasureList_II, lineThreshold, f, f_step, f_upValue):
        self.MeasureList_I = strMeasureList_I
        self.MeasureList_II = strMeasureList_II
        self.lineThreshold = lineThreshold
        self.f = f
        self.step = f_step
        self.upValue = f_upValue
        self.stableDotGroup = []

    def dotGroupSearchAnalysis(self):
        """
        稳定点组逻辑判断
        :param strMeasureList_I: 一期坐标序列：[pointID，X,Y,Z]
        :param strMeasureList_II:
        :param threshold: 共线判定阈值
        :param f: 阈值
        :return:
        """
        strMeasureList_I = self.MeasureList_I
        strMeasureList_II = self.MeasureList_II
        for i in range(len(strMeasureList_I) - 1):  # i,j循环
            # print("========= 第" + str(i) + "次循环======")
            pointI_1 = [float(strMeasureList_I[i][1]), float(strMeasureList_I[i][2]), float(strMeasureList_I[i][3])]
            pointII_1 = [float(strMeasureList_II[i][1]), float(strMeasureList_II[i][2]), float(strMeasureList_II[i][3])]
            pointI_2 = [float(strMeasureList_I[i + 1][1]), float(strMeasureList_I[i + 1][2]),
                        float(strMeasureList_I[i + 1][3])]

            # 判断1 2 点是否很邻近
            pointII_2 = pointI_2
            j_index = 0
            for k in range(i + 1, len(strMeasureList_I) - 1):  # j 检测
                planeDistance = math.sqrt(
                    (pointI_2[0] - pointI_1[0]) * (pointI_2[0] - pointI_1[0]) + (pointI_2[1] - pointI_1[1]) * (
                            pointI_2[1] - pointI_1[1]))
                if planeDistance < self.lineThreshold:  # 选定的两点阈值
                    pointI_2 = [float(strMeasureList_I[k][1]), float(strMeasureList_I[k][2]),
                                float(strMeasureList_I[k][3])]
                    pointII_2 = [float(strMeasureList_II[k][1]), float(strMeasureList_II[k][2]),
                                 float(strMeasureList_II[k][3])]

                else:
                    # j_index = k
                    # 计算平面斜率
                    if (pointI_2[0] - pointI_1[0]) != 0:
                        k_line = (pointI_2[1] - pointI_1[1]) / (pointI_2[0] - pointI_1[0])
                    else:
                        k_line = 0
                    b = pointI_1[1] - k_line * pointI_1[0]
                    # 函数模型 y = k * x + b
                    # print("三个非共线点：", point_1, "\n", point_2, pointIndex, strMeasureList[pointIndex])
                    # print("斜率与尺度：",k,b,"计算第三点：",Y3,y,abs(Y3-y))
                    # 从剩余 n - 2 个点找到第一个与上两点不共线的点
                    pointI_3 = [0, 0, 0]
                    pointII_3 = [0, 0, 0]
                    for ki in range(k + 1, len(strMeasureList_I)):  # k 循环
                        X3 = float(strMeasureList_I[ki][1])
                        Y3 = float(strMeasureList_I[ki][2])
                        # 函数构建
                        y = k_line * X3 - b
                        if abs(Y3 - y) > self.lineThreshold:  # 大于阈值，判定为非共线
                            # print("  -------第{%d}次ij循环，第{%d}个k点：", i,k, ki)
                            pointI_3 = [float(strMeasureList_I[ki][1]), float(strMeasureList_I[ki][2]),
                                        float(strMeasureList_I[ki][3])]

                            pointII_3 = [float(strMeasureList_II[ki][1]), float(strMeasureList_II[ki][2]),
                                         float(strMeasureList_II[ki][3])]
                            pointGroup_I = [pointI_1, pointI_2, pointI_3]
                            pointGroup_II = [pointII_1, pointII_2, pointII_3]
                            result = self.singleDotGroupAnalysis(pointGroup_I, pointGroup_II, self.f, self.step,
                                                                 self.upValue)
                            if result is True:
                                self.stableDotGroup.append([i, k, ki])

    def singleDotGroupAnalysis(self, pointGroup_I, pointGroup_II, f, f_step, upValue):
        """
        点组分析
        :param pointGroup_I:
        :param pointGroup_II:
        :param f:
        :return:
        """
        # 稳定形变监测 尺度因子约等1
        # 七参数转换
        B = []
        L = []
        for i in range(3):
            B.append([1, 0, 0, 0, -pointGroup_I[i][2], -pointGroup_I[i][1], -pointGroup_I[i][0]])
            B.append([0, 1, 0, -pointGroup_I[i][2], 0, pointGroup_I[i][0], pointGroup_I[i][1]])
            B.append([0, 0, 1, pointGroup_I[i][1], pointGroup_I[i][0], 0, pointGroup_I[i][2]])

            L.append([pointGroup_II[i][0] - pointGroup_I[i][0]])
            L.append([pointGroup_II[i][1] - pointGroup_I[i][1]])
            L.append([pointGroup_II[i][2] - pointGroup_I[i][2]])

        matrix_B = np.mat(B)
        matrix_L = np.mat(L)

        # 构造权阵
        P = [[0 for jk in range(9)] for ij in range(9)]  # 9*9 空矩阵
        for i in range(9):
            for k in range(9):
                if i == k:
                    P[i][k] = 1

        matrix_P = np.mat(P)
        # matrix_P = np.mat(1 / self.Dxyz_I)
        # 平差模型计算
        matrix_QR = np.linalg.inv(((np.transpose(matrix_B) * matrix_P * matrix_B)))
        matrix_X = matrix_QR * np.transpose(matrix_B) * matrix_P * matrix_L
        matrix_V = matrix_B * matrix_X - matrix_L
        # c = (np.transpose(matrix_V) * matrix_P * matrix_V)
        theta = np.sqrt((np.transpose(matrix_V) * matrix_P * matrix_V).tolist()[0][0] / 2)

        # teta_X 的协因数阵
        matrix_Qteta = np.linalg.inv(matrix_P)

        # 协因数计算
        matrix_Qv = matrix_Qteta - matrix_B * matrix_QR * np.transpose(matrix_B) - np.linalg.inv(
            matrix_P) - matrix_B * np.linalg.inv(
            np.transpose(matrix_B) * np.linalg.inv(matrix_P) * matrix_B) * np.transpose(matrix_B)
        matrix_Dx = theta * theta * matrix_QR
        # 变换后二期坐标方差
        matrix_Dx_II = theta * theta * matrix_Qv
        # 变换后的二期坐标
        seven_para = matrix_X.tolist()
        B_II = [
            [1, -seven_para[5][0], seven_para[4][0]],
            [seven_para[5][0], 1, -seven_para[3][0]],
            [-seven_para[4][0], seven_para[4][0], 1]
        ]
        changeCoor_II = []  # 3n * 1
        for i in range(3):
            changeCoor_II += (
                (np.mat([[seven_para[0][0]], [seven_para[1][0]], [seven_para[2][0]]]) + (
                        1 + seven_para[6][0]) * np.mat(B_II) * np.mat(
                    [[pointGroup_I[i][0]], [pointGroup_I[i][1]], [pointGroup_I[i][2]]]
                )).tolist()
            )
        # 平移转换后的二期坐标
        changeCoor_II = (np.mat(changeCoor_II) - matrix_L).tolist()
        # print(changeCoor_II)
        # 转换二期坐标与一期观测坐标差
        index = 0
        tetaList = []
        mList = []
        for i in range(3):
            dx = changeCoor_II[index][0] - pointGroup_I[i][0]
            mx = np.sqrt(dx * dx / 3)
            dy = changeCoor_II[index + 1][0] - pointGroup_I[i][1]
            my = np.sqrt(dy * dy / 9)
            dz = changeCoor_II[index + 2][0] - pointGroup_I[i][2]
            mz = np.sqrt(dz * dz / 9)
            index += 3
            tetaList += ([[dx], [dy], [dz]])
            mList += ([[mx], [my], [mz]])
        # 判定条件
        result = self._judge(tetaList, mList, f, f_step, upValue)
        # print("本轮结束！result = ", result)
        if result == 1:
            # print("稳定点组")
            return True
        else:
            # print("非稳定点组，继续....")
            return False

    def _judge(self, teta, m, f, step, upValue):
        while f < upValue:
            injust = 1
            for i in range(3, 9):
                # print("第" + str(i) + "次调整f值：" + str(f) + ",dxi_jk fm", teta[i][0], f * m[i][0])
                if teta[i][0] > f * m[i][0]:
                    injust = 0  # 有一个不合格即为假，非稳定点组
                    # 改变 f 阈值
                    f += step

            if injust == 1:
                return injust
            else:
                return 0

    def getStablePointGroup(self):
        return self.stableDotGroup
