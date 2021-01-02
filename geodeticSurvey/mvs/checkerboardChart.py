#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 生成棋盘标定图

@author: GanAH  2020/9/11.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import cv2
import numpy as np


def generatePattern(CheckerboardCellSize, column_count, row_count):
    '''
    自定义生成棋盘
    :param CheckerboardCellSize: 棋盘格子大小,单位:px
    :param column_count: 棋盘格横向黑白格子数
    :param row_count: 棋盘格纵向黑白格子数
    :return:
    '''
    column_count = column_count - 1
    row_count = row_count - 1

    black = np.zeros((CheckerboardCellSize, CheckerboardCellSize, 3), np.uint8)
    white = np.zeros((CheckerboardCellSize, CheckerboardCellSize, 3), np.uint8)
    black[:] = [0, 0, 0]  # 纯黑色
    white[:] = [255, 255, 255]  # 纯白色

    black_white = np.concatenate([black, white], axis=1)
    black_white2 = black_white
    white_black = np.concatenate([white, black], axis=1)
    white_black2 = white_black

    # 横向连接
    if column_count % 2 == 1:
        for i in range(1, (column_count + 1) // 2):
            black_white2 = np.concatenate([black_white2, black_white], axis=1)
            white_black2 = np.concatenate([white_black2, white_black], axis=1)
    else:
        for i in range(1, column_count // 2):
            black_white2 = np.concatenate([black_white2, black_white], axis=1)
            white_black2 = np.concatenate([white_black2, white_black], axis=1)
        black_white2 = np.concatenate([black_white2, black], axis=1)
        white_black2 = np.concatenate([white_black2, white], axis=1)

    jj = 0
    black_white3 = black_white2
    for i in range(0, row_count):
        jj += 1
        # 纵向连接
        if jj % 2 == 1:
            black_white3 = np.concatenate((black_white3, white_black2))  # =np.vstack((img1, img2))
        else:
            black_white3 = np.concatenate((black_white3, black_white2))  # =np.vstack((img1, img2))

    cv2.imshow('', black_white3)
    cv2.imwrite('pattern.jpg', black_white3, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cv2.waitKey(10000)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    generatePattern(120, 13, 11)
