#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 坐标系转换

@author: GanAH  2020/2/26.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import math
import numpy as np

from algorithm.common.BasicMeasurementAlgorithm import BasicMeasurementAlgorithm


class TwoDissCoorTran():
    def __init__(self):
        pass

    def directParaMethod(self, sourceCoorArrayList_XY, targetArrayDataList_xy):
        """
        二维坐标直接参数转换法

        :param sourceCoorArrayList_XY: 原始坐标系数据 X Y
        :param targetArrayDataList_xy: 待转换目标坐标系数据 x y
        :return: List1 剩余转换后数据，List2[DX DY 中误差]
        """

        # 取出两个公共点坐标对,例如：P1（X1,Y1）-P1'(x1,y1),P2(X2,Y2)--P2'(x2,y2)
        teta_X = sourceCoorArrayList_XY[1][0] - sourceCoorArrayList_XY[0][0]
        teta_Y = sourceCoorArrayList_XY[1][1] - sourceCoorArrayList_XY[0][1]
        teta_x = targetArrayDataList_xy[1][0] - targetArrayDataList_xy[0][0]
        teta_y = targetArrayDataList_xy[1][1] - targetArrayDataList_xy[0][1]

        distXY_S = math.sqrt(teta_X * teta_X + teta_Y * teta_Y)
        distxy_s = math.sqrt(teta_x * teta_x + teta_y * teta_y)
        # 坐标方位角 ，注意需要判断好象限

        A = math.atan(teta_Y / teta_X)
        alpha = math.atan(teta_y / teta_x)

        # basicMea = BasicMeasurementAlgorithm()
        # A = basicMea.calc_angle(sourceCoorArrayList_XY[0][0], sourceCoorArrayList_XY[0][1],
        #                          sourceCoorArrayList_XY[1][0],
        #                          sourceCoorArrayList_XY[1][1])
        # alpha = basicMea.calc_angle(targetArrayDataList_xy[0][0], targetArrayDataList_xy[0][1],
        #                              targetArrayDataList_xy[1][0], targetArrayDataList_xy[1][1])
        # print([A, alpha, A1 * 3.1415926 / 180, alpha1 * 3.1415926 / 180])
        # 平移参数
        Dx1 = sourceCoorArrayList_XY[0][0] - targetArrayDataList_xy[0][0]
        Dy1 = sourceCoorArrayList_XY[0][1] - targetArrayDataList_xy[0][1]
        # 尺度因子
        m = (distxy_s - distXY_S) / distXY_S
        # 旋转参数
        theta = A - alpha

        tranPara = [[Dx1], [Dy1], [m], [theta * 180 / 3.1415926]]

        resultTranList = []
        for i in range(len(sourceCoorArrayList_XY)):
            teta_Xi = sourceCoorArrayList_XY[i][0] - sourceCoorArrayList_XY[0][0]
            teta_Yi = sourceCoorArrayList_XY[i][1] - sourceCoorArrayList_XY[0][1]
            tranMatrix = np.mat([[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]])
            tetaMatrix_xyi = (1 + m) * tranMatrix * np.mat([[teta_Xi], [teta_Yi]])
            matrix_xyi = np.mat([[targetArrayDataList_xy[0][0]], [targetArrayDataList_xy[0][1]]]) + tetaMatrix_xyi

            # 转置解包返回结果为list [[x,y],[x2,y2]...]
            resultTranList += np.transpose(matrix_xyi).tolist()

        return {"para": tranPara, "result": resultTranList}

    def leastSquaresMethod(self, publicPointCount, sourceCoorArrayList_XY, targetArrayDataList_xy):
        """
        最小二乘法计算求解坐标转换四参数
        :param publicPointCount: 公共点数
        :param sourceCoorArrayList_XY: 初始坐标
        :param targetArrayDataList_xy: 转换目的坐标
        :return:dictionary:{sigma,para,result,correct,otherResult} ;
        <p>中误差;参数：二维list[Dx,Dy,seta,dist_m];转换结果：二维list;改正数二维list；其他点转换：二维list
        """
        L = []
        B = []
        for i in range(publicPointCount):
            # 构建L矩阵,后续需要转置
            L.append(targetArrayDataList_xy[i][0])
            L.append(targetArrayDataList_xy[i][1])
            # 构建系数矩阵
            B.append([1, 0, sourceCoorArrayList_XY[i][1], sourceCoorArrayList_XY[i][0]])
            B.append([0, 1, -sourceCoorArrayList_XY[i][0], sourceCoorArrayList_XY[i][1]])

        # 权矩阵为单位阵

        # 进行平差
        matrix_B = np.mat(B)
        matrix_L = np.transpose(np.mat([L]))
        count = 0
        while True:
            matrix_X = (np.linalg.inv(np.transpose(matrix_B) * matrix_B)) * np.transpose(matrix_B) * matrix_L
            matrix_v = matrix_B * matrix_X - matrix_L
            # 找改正数矩阵最大值,由于为二维矩阵，故取数值要注意
            maxValue = np.max(matrix_v, axis=0).tolist()[0][0]
            count += 1
            # 条件判断
            if maxValue < 1E-5:
                # print("循环次数:", count)
                # 改正
                leastResultCorrect = (matrix_L + matrix_v).tolist()
                # 中误差
                sigma = math.sqrt((np.transpose(matrix_v) * matrix_v) / (2 * publicPointCount - 4))
                temp = matrix_X.tolist()
                paraList = [temp[0][0], temp[1][0], temp[2][0], temp[3][0]]
                theta = math.atan(paraList[2] / paraList[3])
                m = paraList[2] / math.sin(theta)
                paraList = [paraList[0], paraList[1], theta, m]

                # 其他点求解
                otherPointChange = []
                for i in range(len(sourceCoorArrayList_XY)):
                    otherPointChange.append(
                        [
                            paraList[0] + sourceCoorArrayList_XY[i][1] * paraList[2] + sourceCoorArrayList_XY[i][0] *
                            paraList[3],
                            paraList[1] - sourceCoorArrayList_XY[i][0] * paraList[2] + sourceCoorArrayList_XY[i][1] *
                            paraList[3]
                        ]
                    )

                # 转换结果拼合
                # allResult = np.insert(otherPointChange, 0, matrix_L, axis=0)
                paraList = [[publicPointCount], [count], [paraList[0]], [paraList[1]], [theta * 180 / 3.1415926], [m],
                            [sigma * 1000]]
                # 封装返回结果
                return {"para": paraList,
                        "correct": np.transpose(matrix_v).tolist(),
                        "resultCorrect": leastResultCorrect,
                        "result": otherPointChange
                        }
            # 迭代限制，以防死循环
            elif count > 30:  # 返回错误提示,用 sigma 替代
                return {"para": [[0], [count], [0], [0], [0]]}
            else:
                matrix_L = matrix_L + matrix_v

    def conformalTransFormationMethod(self, publicPointCount, sourceCoorArrayList_XY, targetArrayDataList_xy):
        """
        普通正形变换法
        :param publicPointCount: 公共点数 >= 6
        :param sourceCoorArrayList_XY: 原始坐标系数据 X Y
        :param targetArrayDataList_xy: 待转换目标坐标系数据 x y
        :return:
        """
        # 构造矩阵
        B = []
        L = []
        for i in range(publicPointCount):
            xi = sourceCoorArrayList_XY[i][0]
            yi = sourceCoorArrayList_XY[i][1]
            # B 矩阵
            B.append([1, 0, xi, -yi, xi * xi - yi * yi, -2 * xi * yi, xi * xi * xi - 3 * xi * yi * yi,
                      yi * yi * yi - 3 * xi * xi * yi, xi ** 4 - 6 * xi * xi * yi * yi + yi ** 4,
                      4 * xi * yi * yi * yi - 4 * xi * xi * xi * yi])
            B.append([0, 1, yi, xi, 2 * xi * yi, xi * xi - yi * yi, 3 * xi * xi * yi - yi * yi * yi,
                      xi * xi * xi - 3 * xi * yi * yi,
                      4 * xi * xi * xi * yi - 4 * xi * yi * yi * yi,
                      xi * xi * xi * xi - 6 * xi * xi * yi * yi + yi ** 4])
            # L矩阵
            L.append([targetArrayDataList_xy[i][0]])
            L.append([targetArrayDataList_xy[i][1]])

        matrix_B = np.mat(B)
        matrix_L = np.mat(L)
        # 平差
        matrix_X = np.linalg.inv((np.transpose(matrix_B)) * matrix_B) * np.transpose(matrix_B) * matrix_L

        matrix_v = matrix_B * matrix_X - matrix_L

        sigma = math.sqrt(((np.transpose(matrix_v) * matrix_v).tolist()[0][0]) / (2 * publicPointCount - 10))

        # 全体转换
        result = []
        for i in range(len(sourceCoorArrayList_XY)):
            xi = sourceCoorArrayList_XY[i][0]
            yi = sourceCoorArrayList_XY[i][1]
            matrix_Bi = np.mat([
                [
                    1, 0, xi, -yi, xi * xi - yi * yi, -2 * xi * yi, xi * xi * xi - 3 * xi * yi * yi,
                                   yi * yi * yi - 3 * xi * xi * yi, xi ** 4 - 6 * xi * xi * yi * yi + yi ** 4,
                                   4 * xi * yi * yi * yi - 4 * xi * xi * xi * yi
                ],
                [
                    0, 1, yi, xi, 2 * xi * yi, xi * xi - yi * yi, 3 * xi * xi * yi - yi * yi * yi,
                                  xi * xi * xi - 3 * xi * yi * yi,
                                  4 * xi * xi * xi * yi - 4 * xi * yi * yi * yi,
                                  xi * xi * xi * xi - 6 * xi * xi * yi * yi + yi ** 4
                ]
            ])
            result.append(np.transpose(matrix_Bi * matrix_X).tolist()[0])

        # 降维并转换
        paraList = matrix_X.tolist()
        # 在第一位插入公共点个数
        paraList.insert(0, [sigma])
        paraList.insert(0, [publicPointCount])

        # 转换数组维度
        return {"para": paraList,
                "correct": matrix_v.tolist(),
                "correctResult": (matrix_v + matrix_L).tolist(),
                "result": result
                }

    def conformalTransFormationMethod_Premium(self, publicPointCount, sourceCoorArrayList_XY, targetArrayDataList_xy):
        """
        优化的正形变换法
        :param publicPointCount: 公共点数 >= 5
        :param sourceCoorArrayList_XY: 原始坐标系数据 X Y
        :param targetArrayDataList_xy: 待转换目标坐标系数据 x y
        :return:
        """
        # 优化B矩阵结构的常数，取平均值 注意！！！！ 这是一个壮举，利用这种方式来求二维list某一列的和！！！
        average_X = sum([sourceCoorArrayList_XY[i][0] for i in range(publicPointCount)]) / publicPointCount
        average_Y = sum([sourceCoorArrayList_XY[i][1] for i in range(publicPointCount)]) / publicPointCount

        maxDistance = 0
        index = 0
        # 计算最大距离,以已知点第一数为参照，目标依次计算
        for i in range(1, publicPointCount):
            teta_Xx = sourceCoorArrayList_XY[0][0] - targetArrayDataList_xy[i][0]
            teta_Yy = sourceCoorArrayList_XY[0][1] - targetArrayDataList_xy[i][1]
            distance = math.sqrt(teta_Xx * teta_Xx + teta_Yy * teta_Yy)
            if maxDistance < distance:
                maxDistance = distance
                index = i
        # 第一次线性变换公式
        matrix_b_dot = np.mat([[1, 0, sourceCoorArrayList_XY[0][0], -sourceCoorArrayList_XY[0][1]],
                               [0, 1, sourceCoorArrayList_XY[0][1], sourceCoorArrayList_XY[0][0]],
                               [1, 0, sourceCoorArrayList_XY[index][0], -sourceCoorArrayList_XY[index][1]],
                               [0, 1, sourceCoorArrayList_XY[index][1], sourceCoorArrayList_XY[index][0]]])

        coffP = (np.linalg.inv(matrix_b_dot) * np.mat(
            [[targetArrayDataList_xy[0][0]],
             [targetArrayDataList_xy[0][1]],
             [targetArrayDataList_xy[index][0]],
             [targetArrayDataList_xy[index][1]]])).tolist()

        # 构造矩阵
        B = []
        L = []

        for i in range(publicPointCount):
            xi = sourceCoorArrayList_XY[i][0] - average_X
            yi = sourceCoorArrayList_XY[i][1] - average_Y
            # B 矩阵
            B.append([1, 0, xi, -yi, xi * xi - yi * yi, -2 * xi * yi, xi * xi * xi - 3 * xi * yi * yi,
                      yi * yi * yi - 3 * xi * xi * yi, xi ** 4 - 6 * xi * xi * yi * yi + yi ** 4,
                      4 * xi * yi * yi * yi - 4 * xi * xi * xi * yi])
            B.append([0, 1, yi, xi, 2 * xi * yi, xi * xi - yi * yi, 3 * xi * xi * yi - yi * yi * yi,
                      xi * xi * xi - 3 * xi * yi * yi,
                      4 * xi * xi * xi * yi - 4 * xi * yi * yi * yi,
                      xi * xi * xi * xi - 6 * xi * xi * yi * yi + yi ** 4])
            # L矩阵
            L.append([targetArrayDataList_xy[i][0] - coffP[0][0] - sourceCoorArrayList_XY[i][0] * coffP[2][0] +
                      sourceCoorArrayList_XY[i][1] * coffP[3][0]])
            L.append([targetArrayDataList_xy[i][1] - coffP[1][0] - sourceCoorArrayList_XY[i][0] * coffP[2][0] -
                      sourceCoorArrayList_XY[i][0] * coffP[3][0]])

        matrix_B = np.mat(B)
        matrix_L = np.mat(L)
        # 平差
        matrix_X = np.linalg.inv((np.transpose(matrix_B)) * matrix_B) * np.transpose(matrix_B) * matrix_L

        matrix_v = matrix_B * matrix_X - matrix_L

        sigma = math.sqrt(((np.transpose(matrix_v) * matrix_v).tolist()[0][0]) / (2 * publicPointCount - 10))

        # 降维并转换
        paraList = matrix_X.tolist()

        # 全体转换
        result = []
        for i in range(len(sourceCoorArrayList_XY)):
            xi = sourceCoorArrayList_XY[i][0]
            yi = sourceCoorArrayList_XY[i][1]
            matrix_Bi = np.mat([
                [
                    1, 0, xi, -yi, xi * xi - yi * yi, -2 * xi * yi, xi * xi * xi - 3 * xi * yi * yi,
                                   yi * yi * yi - 3 * xi * xi * yi, xi ** 4 - 6 * xi * xi * yi * yi + yi ** 4,
                                   4 * xi * yi * yi * yi - 4 * xi * xi * xi * yi
                ],
                [
                    0, 1, yi, xi, 2 * xi * yi, xi * xi - yi * yi, 3 * xi * xi * yi - yi * yi * yi,
                                  xi * xi * xi - 3 * xi * yi * yi,
                                  4 * xi * xi * xi * yi - 4 * xi * yi * yi * yi,
                                  xi * xi * xi * xi - 6 * xi * xi * yi * yi + yi ** 4
                ]
            ])

            res = matrix_Bi * matrix_X

            result.append(np.transpose(matrix_Bi * matrix_X).tolist()[0])

        print(result)

        paraList.insert(0, [publicPointCount])

        # 转换数组维度
        return {
            "para": paraList,
            "correct": matrix_v.tolist(),
            "correctResult": (matrix_v + matrix_L).tolist(),
            "result": result
        }

    def calc_angle(self, x1, y1, x2, y2):
        angle = 0
        dy = y2 - y1
        dx = x2 - x1
        if dx == 0 and dy > 0:
            angle = 0
        if dx == 0 and dy < 0:
            angle = 180
        if dy == 0 and dx > 0:
            angle = 90
        if dy == 0 and dx < 0:
            angle = 270
        if dx > 0 and dy > 0:
            angle = math.atan(dx / dy) * 180 / math.pi
        elif dx < 0 and dy > 0:
            angle = 360 + math.atan(dx / dy) * 180 / math.pi
        elif dx < 0 and dy < 0:
            angle = 180 + math.atan(dx / dy) * 180 / math.pi
        elif dx > 0 and dy < 0:
            angle = 180 + math.atan(dx / dy) * 180 / math.pi
        return angle

    def oneRowToMoreRow(self, List):
        """
        将二维list单列截取凑到行，如10*1-->5*2
        :param List: 初始
        :param lenRow: 目标列数
        :return: list
        """
        result = []
        for i in range(0, len(List), 2):
            result.append([List[i][0], List[i + 1][0]])
        return result


class threeDissCoorTran():
    def __init__(self):
        pass
