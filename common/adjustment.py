#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2019/12/19.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import numpy as np

class Adjustment():
    def indirect_adjustment(self, B, P, L):
        """
        间接平差模型
        <p>矩阵传入list格式
        :param B: 系数B矩阵
        :param P: 权阵
        :<p>单位阵的维度与B的行数相同
        :param L:L矩阵
        :<p>尤其注意此处的L矩阵， v = Bx - L
        :return: matrix_x,matrix_V
        """
        matrix_B = np.mat(B)
        matrix_P = np.mat(P)
        matrix_L = np.mat(L)

        # 间接平差解算
        matrix_Nbb = (np.transpose(matrix_B) * matrix_P * matrix_B)
        matrix_Nbbinver = np.linalg.inv(matrix_Nbb)

        matrix_W = (np.transpose(matrix_B) * matrix_P * matrix_L)

        # 解算x矩阵
        matrix_x = matrix_Nbbinver * matrix_W
        # 解算改正数矩阵V
        matrix_V = matrix_B * matrix_x - matrix_L

        return matrix_x, matrix_V

    def condition_adjustment(self,A,P):
        """
        条件平差模型
        :param A:
        :param P:
        :return:
        """
        pass

