#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2020/5/23.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from __future__ import division, print_function, absolute_import

import time
import warnings
from collections import defaultdict

import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto

config = ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from PIL.Image import Image
from PyQt5.QtCore import pyqtSignal, QThread

from MTD.tools import box_filter
from MTD.tools.plot_utils import *
from MTD.license_plate_recognition import *
from MTD.yolo import YOLO

from database.database import Database
from database.imageQueue import Queue
from loggerConfig.logger import Logger


class ActionPicturesDetectionThread(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()

    def __init__(self):
        super(ActionPicturesDetectionThread, self).__init__()
        self.logger = Logger().get_logger("MTD_ACTION_THREAD")

    def setPara(self, *args):
        self.type = args[0]["type"]
        self.COI = args[0]["COI"]
        self.dict = args[0]

    def run(self) -> None:
        self._sendInfo("I", "子线程已开启....")
        try:
            # 预启动模型
            yolo = Database.yoloModel
            if isinstance(yolo, property):  # 模型不存在，初始化并存入数据库
                # 提示等待模型加载
                self._sendInfo("V", "检测到当前为初次使用，需要预加载模型以提高速度，后续将不再需要加载，请耐心等待片刻")
                self._sendInfo("T", "检测到当前为初次使用，需要预加载模型\n以提高速度，后续将不再需要加载。")
                self.initializeYolo()
                # 从数据库获取模型
                yolo = Database.yoloModel
            self._sendInfo("I", "模型加载完成")
            if self.type == "201":
                self.singleImageDetection(yolo)
            elif self.type == "202":
                self.imagesDetection(yolo)
            else:  # 虚位以待其他功能
                pass
            self._sendInfo("V", "完成目标检测")
            # 结束，发送终止信号
            self.overEmit.emit()
        except Exception as e:
            self._sendInfo("E", "异常警告：" + e.__str__())

    def initializeYolo(self):
        # TODO 条件控制
        score_thre = 0.3
        iou_thre = 0.3
        Database.yoloModel = YOLO(model_path=Database.modelPath,
                                  classes_path=Database.classes_path,
                                  weights_only=True,
                                  score=score_thre,
                                  iou=iou_thre)  # coco version

    def singleImageDetection(self, yolo):
        """
        单项检测功能：car ,bike and all
        :return:
        """
        self._sendInfo("V", "模型加载完成，单张图像检测中")
        self._sendInfo("I", "\n- 单张图像检测中.....")
        image = Image.open(self.dict["path"])
        # 是否存储
        autoSave = self.dict["autoSave"]
        # 识别模式
        detectionMode = self.dict["mode"]
        if detectionMode == 0:
            image, quantity = self.findCertainCatgory(yolo, image, self.COI)
            sum = 0
            for v in quantity.values():
                sum += v
            self._sendInfo("I", "Totally has " + str(sum) + " objects.")
            for k, v in quantity.items():
                if v != 0:
                    self._sendInfo("I", "has " + str(v) + " " + k)
        else:
            image = self.detectObjectAndLicensePlate(yolo, image, self.COI)
            quantity = {
                "None": None
            }
        # 存入数据库并显示到界面
        Database.imageResult = {"image": image, "COI": quantity}
        self._sendInfo("A", None)
        if autoSave:  # 自动保存
            (dir, imageName) = os.path.split(self.dict["path"])
            self.autoSaveImage(image, imageName)

    def imagesDetection(self, yolo):
        imagesPathList = self.dict["path"]
        self._sendInfo("V", "模型加载完成，多张图像检测中")
        self._sendInfo("I", "模型加载完成，多张图像检测中.....")
        # 获取显示方式
        showWait = self.dict["show"]
        # 是否存储
        autoSave = self.dict["autoSave"]
        # 识别模式
        detectionMode = self.dict["mode"]
        for i in range(len(imagesPathList)):
            (dir, imageName) = os.path.split(imagesPathList[i])
            self._sendInfo("I", "\n  - 第" + str(i + 1) + "张图像: " + imageName + " 检测中...")
            image = Image.open(imagesPathList[i])
            w, h = image.size
            if detectionMode == 0:
                resultImage, quantity = self.findCertainCatgory(yolo, image, self.COI, w // 100)
                # output result
                sum = 0
                for v in quantity.values():
                    sum += v
                self._sendInfo("I", "Totally has " + str(sum) + " objects.")
                for k, v in quantity.items():
                    if v != 0:
                        self._sendInfo("I", "has " + str(v) + " " + k)
            else:
                resultImage = self.detectObjectAndLicensePlate(yolo, image, self.COI, w // 100, w // 300)
                quantity = {"None": None}

            if showWait:  # 显示方式
                # 加一点小延迟，以便看出图像在切换
                time.sleep(0.5)
                # 加入队列并发送已完成信号
                Queue().imageStrak(resultImage)
                Queue().setImageCOI(quantity)
                self._sendInfo("M", None)
            else:
                self.pltShowImage(resultImage, "RESULT_IMAGES")
                # TODO 验证该方法是否在不同环境均可实现_依赖运行环境的图像浏览工具
                # resultImage.show()

            if autoSave:  # 自动保存
                self.autoSaveImage(resultImage, imageName)

    def _sendInfo(self, type, infoStr):
        """
        线程信号发射
        :return:
        """
        if type == "I":
            self.logger.info(infoStr)
        self.infoEmit.emit(type, infoStr)

    def killThread(self):
        """
        结束线程
        :return:
        """
        self.terminate()

    def pltShowImage(self, image, title):
        plt.figure(title)
        plt.imshow(image)
        plt.show()

    def autoSaveImage(self, image, imageName):
        dir = Database.workspace + "/Image_Result"
        # 判断是否存在，不存在创建
        if os.path.exists(dir) is False:
            os.mkdir(dir)
        path = dir + "/RESULT_" + imageName
        print("S", path, type(image))
        image.save(path)
        self._sendInfo("I", "已自动保存识别结果到工作空间，路径：" + path)

    def findCertainCatgory(self, yolo, img, COI=None, max_bbox_overlap=0.5, fontsize=15):
        '''
        检测图像中某一特定类别的物体，并统计数量
        =============
        Parameters:
            yolo: 一个YOLO对象
            img: PIL图像 -> 要检测的图像
            COI: list -> 感兴趣的类别,可以有多个
            max_bbox_overlap : IOU阈值，筛去重叠物体

        Return:
            img_res: PIL图像 -> 显示检测结果
            quantity: dict -> 每一类的数量
                eg.{ "car": 2, "bicycle": 5, "truck": 1 ......}
        '''
        quantity = defaultdict(int)

        # 感兴趣的类别中有无法检测的类别时
        if COI != None:
            quantity = {c: 0 for c in COI}
            for c in COI:
                if c not in yolo.class_names:
                    self._sendInfo("I", c + " can't be detected.")
                    return img, quantity

        img_res = img.copy()
        boxes, classes, scores = yolo.detect_image(img_res)  # detect
        boxes, classes, scores = box_filter.non_max_suppression(boxes, classes, scores,
                                                                max_bbox_overlap)  # none max suppression
        if COI != None:
            boxes, classes, scores = box_filter.select_classes(boxes, classes, scores, COI)  # select category

        img_res = draw_detection_boxes(img_res, yolo, boxes, classes, scores, fontsize=fontsize)
        for cat in classes:
            quantity[cat] += 1

        return img_res, quantity

    def detectObjectAndLicensePlate(self, yolo, img, COI=None, max_bbox_overlap=0.5,
                                    fontsize=15, thickness=5):
        """
        车牌号识别
        ============
        Parameters:
            yolo: 一个YOLO对象
            img: PIL图像 -> 要检测的图像
            COI: list -> 感兴趣的类别,可以有多个
            max_bbox_overlap : IOU阈值，筛去重叠物体

        Return:
            img_res: PIL图像 -> 显示检测结果
        """

        img_res = img.copy()

        boxes, classes, scores = yolo.detect_image(img_res)  # detect
        boxes, classes, scores = box_filter.non_max_suppression(boxes, classes, scores,
                                                                max_bbox_overlap)  # none max suppression
        if COI != None:
            boxes, classes, scores = box_filter.select_classes(boxes, classes, scores, COI)  # select category

        # 在框内进行车牌号检测
        license_plates, plate_scores, plate_boxes = lprBasedYOLO(img, boxes, classes)

        img_res = draw_detection_boxes(img_res, yolo, boxes, classes, scores, fontsize=fontsize)

        for i, bbox in enumerate(plate_boxes):
            label = "%s\n%.3f" % (license_plates[i], plate_scores[i])
            img_res = draw_box(img_res, bbox, label, (255, 0, 0), fontsize=fontsize, thickness=thickness)

        return img_res
