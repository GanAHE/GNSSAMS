#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: Camera internal reference estimation

@author: GanAH  2020/9/11.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import glob

from pyexiv2 import Image
import numpy as np
import cv2
from tqdm import tqdm
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

    def getPara_CHESE(self, standardPicDir):
        """
        棋盘法（张正友法）获取相机内参
        :param standardPicDir: 标准像片
        :return:
        """
        # 设置棋盘板长宽
        chessboard_size = (9, 6)

        # 定义数组存储检测到的点
        obj_points = []  # 真实世界中的三维坐标
        img_points = []  # 图片平面的二维坐标

        ####准备目标坐标 （0，0，0），（1，0，0）...（9，6，0）
        # 设置世界坐标下的坐标值
        # 假设棋盘正好在x-y平面上，z直接取零，从而简化初始步骤
        # objp包含的是10*7每一角点的坐标
        objp = np.zeros((np.prod(chessboard_size), 3), np.float32)  # 9*6个三维坐标
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

        # 读取图片，使用glob文件名管理工具
        calibration_paths = glob.glob(standardPicDir + "/*.JPG")

        # 对每张图片，识别出角点，记录世界物体坐标和图像坐标
        for img_path in tqdm(calibration_paths):
            # tqdm是进度条，以了解距离处理上一个图像多长时间，还剩多少图像没有处理
            # 加载图片
            img = cv2.imread(img_path)
            # 照片太大 缩小一半 (不能缩小!!!!内参会变！！像素变小了 并不是对原图像处理)
            # img = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #
            # cv2.imshow('i',img)
            # cv2.waitKey(0)
            # 寻找角点将其存入corners(该图片9*6个角点坐标)，ret是找到角点的标志(True/False)
            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            if ret == True:
                # 检测到角点执行以下操作（一般都能检测到角点，除非图片不是规定的棋盘格）
                # 定义角点精准化迭代过程的终止条件 （包括精度和迭代次数）
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0010)
                # 执行亚像素级角点检测
                corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)

                obj_points.append(objp)
                img_points.append(corners2)

            # 可视化角点
            # img = cv2.drawChessboardCorners(gray,(9,6),corners2,ret)
            # cv2.imshow('s',img)
            # cv2.waitKey(100)

        # 相机标定
        # 每张图片都有自己的旋转和平移矩阵 但是相机内参是畸变系数只有一组（因为相机没变，焦距和主心坐标是一样的）
        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
        saveDir = "./t/"
        # 保存参数
        np.save(saveDir + "ret", ret)
        np.save(saveDir + "K", K)
        np.save(saveDir + "dist", dist)
        np.save(saveDir + "rvecs", rvecs)
        np.save(saveDir + "tvecs", tvecs)

        print(K)

    def read_npy(self, filePath):
        # 模型文件（.npy）部分内容如下：由一个字典组成，字典中的每一个键对应一层网络模型参数。（包括权重w和偏置b）
        a = {'conv1': [array([[1, 2], [3, 4]], dtype=float32), array([5, 6], dtype=float32)],
             'conv2': [array([[1, 2], [3, 4]], dtype=float32), array([5, 6], dtype=float32)]}
        conv1_w = a['conv1'][0]
        conv1_b = a['conv1'][1]
        conv2_w = a['conv2'][0]
        conv2_b = a['conv2'][1]
        print(conv1_w)
        print(tf.Variable(conv1_w))
        print(conv1_b)
        print(tf.Variable(conv1_b))


if __name__ == "__main__":
    cp = CameraInternalReferenceEstimation()
    cp.getPara_PICTURE_EXIF(r"‪E:\CodePrograme\Python\EMACS\workspace\3Dimess\3A_black\IMG_20200918_103413.jpg")
    # cp.getPara_CHESE("./t/")

