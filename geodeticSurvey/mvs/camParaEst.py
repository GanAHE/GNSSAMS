#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: Camera internal reference estimation

@author: GanAH  2020/9/11.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

from pyexiv2 import Image
import cv2
import numpy as np
from numpy import *  # 使用numpy的属性且不需要在前面加上numpy


# import tensorflow as tf


class CameraInternalReferenceEstimation():
    """
    相机内参数标定估计
    """

    def __init__(self):
        pass

    def getPara_PICTURE_EXIF(self, standardPicDir):
        """
        从图像EXIF参数中获取相机参数
        :param standardPicDir: 标准像片
        :return:
        """
        # CMOS长宽信息
        w_c = 6.29
        h_c = 5.21

        # 读取图片的长宽信息
        img = cv2.imread(standardPicDir)
        h = img.shape[0]
        w = img.shape[1]
        print(w, h)

        # 从EXIF中读取焦距
        i = Image(standardPicDir)
        a, b = i.read_exif().get('Exif.Photo.FocalLength').split('/')
        fm = int(a) / int(b)
        f = w * fm / w_c

        # 计算内参信息
        K = np.zeros((3, 3))
        K[0][0] = f
        K[1][1] = f
        K[0][2] = w / 2
        K[1][2] = h / 2
        print(K)


if __name__ == "__main__":
    cp = CameraInternalReferenceEstimation()
    cp.getPara_PICTURE_EXIF(r"E:\CodePrograme\Python\EMACS\workspace\3Dimess\stack\IMG_20200918_181326.jpg")
    # cp.getPara_CHESE("./t/")
