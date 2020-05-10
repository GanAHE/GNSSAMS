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

from window.file.operationFile import OperationFile


class StablePointGroup(object):

    def __init__(self, measureI, measureII, Dxyz_I, Dxyz_II):
        """
        初始化
        :param measureI: 字符型一期测量数据List: ID，X，Y，Z
        :param measureII: 字符型二期测量数据List: ID，X，Y，Z
        """
        self.strMeasureI = measureI
        self.strMeasureII = measureII
        self.Dxyz_I = Dxyz_I
        self.Dxyz_II = Dxyz_II

    def analysis(self, pointGroup_I, pointGroup_II, f):
        # 取第一第二个点与point3Index比对
        pointGroup_I = self._notInLine(self.strMeasureI, 20)
        pointGroup_II = self._notInLine(self.strMeasureII, 60)
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
        c = (np.transpose(matrix_V) * matrix_P * matrix_V)
        theta = np.sqrt((np.transpose(matrix_V) * matrix_P * matrix_V).tolist()[0][0] / (9 - 7))

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
        result = self._judge(tetaList, mList, f)
        print("本轮结束！")
        if result == 1:
            print("稳定")
        else:
            print("非稳定点，继续....")
        # injust = 1
        # for i in range(3, 9):
        #     if tetaList[i][0] >= f * mList[i][0]:
        #         injust = 0  # 有一个不合格即为假，非稳定点组

    def _judge(self, teta, m, f):
        while f < 10:
            injust = 1
            for i in range(3, 9):
                print("dxijk fm", teta[i][0], f * m[i][0])
                if teta[i][0] >= f * m[i][0]:
                    injust = 0  # 有一个不合格即为假，非稳定点组
                    # 改变 f 阈值
                    f += 0.25
            if injust == 1:
                return injust
            else:
                return 0

    def _notInLine(self, strMeasureList, threshold):
        point_1 = [float(strMeasureList[0][1]), float(strMeasureList[0][2]), float(strMeasureList[0][3])]
        point_2 = [float(strMeasureList[1][1]), float(strMeasureList[1][2]), float(strMeasureList[1][3])]

        # 判断1 2 点是否很邻近
        for i in range(1, len(strMeasureList)):
            planeDistance = math.sqrt(
                (point_2[0] - point_1[0]) * (point_2[0] - point_1[0]) + (point_2[1] - point_1[1]) * (
                        point_2[1] - point_1[1]))
            if planeDistance < threshold * 10:  # 选定的两点阈值
                point_2 = [float(strMeasureList[i][1]), float(strMeasureList[i][2]), float(strMeasureList[i][3])]
            else:
                break
        # 计算平面斜率
        k = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        b = point_1[1] - k * point_1[0]
        # 函数模型 y = k * x + b
        # 从剩余 n - 2 个点找到第一个与上两点不共线的点
        pointIndex = 2
        for i in range(2, len(strMeasureList)):
            X3 = float(strMeasureList[i][1])
            Y3 = float(strMeasureList[i][2])
            # 函数构建
            y = k * X3 - b
            pointIndex = i
            if abs(Y3 - y) > threshold:  # 小于阈值，判定为非共线
                break
        # print("三个非共线点：", point_1, "\n", point_2, pointIndex, strMeasureList[pointIndex])
        # print("斜率与尺度：",k,b,"计算第三点：",Y3,y,abs(Y3-y))
        point_3 = [float(strMeasureList[pointIndex][1]), float(strMeasureList[pointIndex][2]),
                   float(strMeasureList[pointIndex][3])]
        return [point_1, point_2, point_3]


if __name__ == "__main__":
    # 读取文件
    measureI = []
    measure_II = []
    filedir = "E:\\CodePrograme\\Python\\EMACS\\source\\测试数据\\稳定点组\\"
    fileData1 = OperationFile().readlargeFile(filedir + "I.xyz")
    fileData2 = OperationFile().readlargeFile(filedir + "II.xyz")
    for i in range(len(fileData1)):
        measureI.append(fileData1[i].split(","))
        measure_II.append(fileData2[i].split(","))
    StablePointGroup(measureI, measure_II, None, None).analysis(None, None, 0.26)
