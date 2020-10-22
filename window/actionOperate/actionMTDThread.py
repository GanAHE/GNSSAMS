#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2020/5/23.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from __future__ import division, print_function, absolute_import
from __future__ import division, print_function, absolute_import

import time
import warnings
from collections import defaultdict

import cv2
import tensorflow as tf
# set config to initialize cudnn
from tensorflow.compat.v1 import ConfigProto

from MTD.deep_sort.detection import Detection
from MTD.deep_sort.tracker import Tracker
from MTD.yolo import YOLO

config = ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from PIL.Image import Image
from PyQt5.QtCore import pyqtSignal, QThread
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

from MTD.tools import box_filter
from MTD.tools.plot_utils import *
from MTD.license_plate_recognition import *
from MTD.tools import generate_detections as gdet
from database.database import Database
from database.imageQueue import Queue
from loggerConfig.logger import Logger

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

warnings.filterwarnings('ignore')


class ActionMTDThread(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()
    stopVideoDetectionEmit = pyqtSignal()
    modelExist = False
    stopCode = 0

    def __init__(self):
        super(ActionMTDThread, self).__init__()
        self.logger = Logger().get_logger("MTD_ACTION_THREAD")

    def setPara(self, *args):
        self.type = args[0]["type"]
        self.COI = args[0]["COI"]
        self.dict = args[0]

    def setViolenceStop(self):
        self.stopCode = 1

    def run(self) -> None:
        self._sendInfo("I", "子线程已开启....")
        try:
            # 预启动模型
            if self.modelExist is False:  # 模型不存在，初始化并存入数据库
                # 提示等待模型加载
                self._sendInfo("V", "检测到当前为初次使用，需要预加载模型以提高速度，后续将不再需要加载，请耐心等待片刻")
                self._sendInfo("T", "检测到当前为初次使用，需要预加载模型\n以提高速度，后续将不再需要加载。")
                self.initializeYolo()
            # 从数据库获取模型
            yolo = Database().getYoloModel()
            self._sendInfo("I", "模型加载完成")
            if self.type == "200":
                # 视频识别-无保存
                self.videoDetection(yolo)
            elif self.type == "201":
                self.singleImageDetection(yolo)
            elif self.type == "202":
                self.imagesDetection(yolo)
            else:
                pass
            self._sendInfo("V", "完成目标检测")
        except Exception as e:
            self._sendInfo("E", "异常警告：" + e.__str__())

    def initializeYolo(self):
        # TODO 条件控制
        score_thre = 0.3
        iou_thre = 0.3
        yolo = YOLO(model_path=Database.modelPath,
                    classes_path=Database.classes_path,
                    weights_only=True,
                    score=score_thre,
                    iou=iou_thre)  # coco version
        Database().setYoloModel(yolo)
        self.modelExist = True

    def videoDetection(self, yolo):
        self._sendInfo("V", "模型加载完成，视频检测中")
        self._sendInfo("I", "视频检测中.....")
        video_handle = self.dict["path"]
        self.track_video(yolo, video_handle, COI=self.COI, det_only=self.dict["onlyDect"],
                         writeVideo_flag=self.dict["avi"])
        self._sendInfo("videoDetecting", None)
        # 结束，发送终止信号
        self.overEmit.emit()

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
            quantity = {"None": None}
        # 存入数据库并显示到界面
        Database.imageResult = {"image": image, "COI": quantity}
        self._sendInfo("A", None)
        if autoSave:  # 自动保存
            (dir, imageName) = os.path.split(self.dict["path"])
            self.autoSaveImage(image, imageName)
        # 结束，发送终止信号
        self.overEmit.emit()

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
            if detectionMode == 0:
                resultImage, quantity = self.findCertainCatgory(yolo, image, self.COI)
                # output result
                sum = 0
                for v in quantity.values():
                    sum += v
                self._sendInfo("I", "Totally has " + str(sum) + " objects.")
                for k, v in quantity.items():
                    if v != 0:
                        self._sendInfo("I", "has " + str(v) + " " + k)
            else:
                resultImage = self.detectObjectAndLicensePlate(yolo, image, self.COI)

            if showWait:  # 显示方式
                # 加一点小延迟，以便看出图像在切换
                time.sleep(0.5)
                # 加入队列并发送已完成信号
                Queue().imageStrak(resultImage)
                self._sendInfo("M", None)
            else:
                self.pltShowImage(resultImage, "RESULT_IMAGES")

                # TODO 验证该方法是否在不同环境均可实现_依赖运行环境的图像浏览工具
                # resultImage.show()

            if autoSave:  # 自动保存
                self.autoSaveImage(resultImage, imageName)
        # 结束，发送终止信号
        self.overEmit.emit()

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

    def track_video(self, yolo, video_handle=Database.modelPath, det_only=False, writeVideo_flag=False, COI=None):
        '''Track objects in a video
        Parameters:
        -----------
            yolo: a class define YOLO algorithm
            video_handle: 0 or video path
            det_only: Bool
                if det_only==True, 只检测不跟踪
        Return:
        -------
            None
        '''
        # create feature encoder
        model_filename = Database.model_filename
        encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        # create tracker
        tracker = Tracker(metric_mode="cosine", max_cosine_distance=0.3,
                          lambda0=1, nn_budget=None)

        video_capture = cv2.VideoCapture(video_handle)

        if writeVideo_flag:
            # Define the codec and create VideoWriter object
            w = int(video_capture.get(3))
            h = int(video_capture.get(4))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            (dir, videoName) = os.path.split(video_handle)
            videoName = videoName.split(".")[0]
            out = cv2.VideoWriter(Database.workspace + "/" + videoName + "_Detection.avi", fourcc, 15, (w, h))
            list_file = open(Database.workspace + "/" + videoName + "_Detection.txt", 'w')
            frame_index = -1

        fps = 0.0
        while True:
            # 检测终止是否有信号
            if self.stopCode != 1:
                ret, frame = video_capture.read()  # frame shape 640*480*3
                if ret != True:
                    break
                t1 = time.time()

                # detect object
                image = Image.fromarray(frame[..., ::-1])  # bgr to rgb,CV to PIL
                boxes, classes, scores = yolo.detect_image(image)  # detect
                # filter boxes
                if COI is not None:
                    boxes, classes, scores = box_filter.select_classes(boxes, classes, scores, COI)
                iou_thre = 0.3
                boxes, classes, scores = box_filter.non_max_suppression(boxes, classes, scores, iou_thre)
                # thickness = 150
                # boxes, classes, scores = box_filter.remove_edge(boxes,classes,scores,thickness,(w,h))

                # encoder features
                features = encoder(frame, boxes)
                detections = [Detection(bbox, score, class_, feature)
                              for bbox, score, class_, feature in zip(boxes, scores, classes, features)]

                # Call the tracker
                tracker.predict()
                tracker.update(detections)

                # detect only, not to track
                if det_only:
                    for bbox, score, cat in zip(boxes, scores, classes):
                        color = yolo.colors[yolo.class_names.index(cat)]
                        bbox = np.array(bbox)
                        bbox[2:] = bbox[:2] + bbox[2:]  # tlwh to tlbr
                        image = draw_detection_box(image, bbox, score, cat, color)
                else:
                    for i, track in enumerate(tracker.tracks):
                        if not track.is_confirmed() or track.time_since_update > 1:
                            continue
                        bbox = track.to_tlbr()
                        image = draw_tracking_box(image, bbox, track.track_id, track.object_class,
                                                  yolo.colors[yolo.class_names.index(track.object_class)])
                img_show = np.asarray(image)[..., ::-1]
                img_pil = Image.fromarray(img_show)
                # 加入队列并发送已完成信号
                Queue().imageStrak(img_pil)
                self._sendInfo("M", None)

                if writeVideo_flag:
                    # save a frame
                    out.write(img_show)
                    frame_index = frame_index + 1
                    list_file.write(str(frame_index) + ' ')
                    if len(boxes) != 0:
                        for i in range(0, len(boxes)):
                            list_file.write(
                                str(boxes[i][0]) + ' ' + str(boxes[i][1]) + ' ' + str(boxes[i][2]) + ' ' + str(
                                    boxes[i][3]) + ' ')
                    list_file.write('\n')

                fps = (fps + (1. / (time.time() - t1))) / 2
                self._sendInfo("F", str(fps))

                # Press Q to stop!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                self._sendInfo("I", "退出循环...")
                self.stopCode = 0
                break

        video_capture.release()
        if writeVideo_flag:
            out.release()
            list_file.close()
        cv2.destroyAllWindows()

    def findCertainCatgory(self, yolo, img, COI=None, max_bbox_overlap=0.5):
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

        img_res = draw_detection_boxes(img_res, yolo, boxes, classes, scores, fontsize=15)
        for cat in classes:
            quantity[cat] += 1

        return img_res, quantity

    def detectObjectAndLicensePlate(self, yolo, img, COI=None, max_bbox_overlap=0.5):
        """
        检测图像中的道路使用者，并进行车牌号识别
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

        img_res = draw_detection_boxes(img_res, yolo, boxes, classes, scores, fontsize=15)

        for i, bbox in enumerate(plate_boxes):
            label = "%s\n%.3f" % (license_plates[i], plate_scores[i])
            img_res = draw_box(img_res, bbox, label, (255, 0, 0), fontsize=15, thickness=5)

        return img_res
