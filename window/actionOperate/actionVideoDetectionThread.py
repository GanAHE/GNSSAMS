#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 视频识别模块

@author: GanAH  2020/7/11.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import cv2
from PyQt5.QtCore import QThread, pyqtSignal

from MTD.tools.coord_utils import computeObjectVelocity, judgeState, MotionState
from MTD.tools.data_utils import load_P
from MTD.tools.plot_utils import *
from MTD.license_plate_recognition import *
from MTD.tools import generate_detections as gdet, box_filter
from MTD.deep_sort.detection import Detection
from MTD.deep_sort.tracker import Tracker
from MTD.deep_sort.track import OverspeedTrack
from MTD.yolo import YOLO
from database.database import Database
from database.imageQueue import Queue
from loggerConfig.logger import Logger
import time


class ActionVideoDetectionThread(QThread):
    infoEmit = pyqtSignal(str, str)
    overEmit = pyqtSignal()
    stopVideoDetectionEmit = pyqtSignal()
    stopCode = 0
    queue = Queue()
    reportLine = []

    def __init__(self):
        super(ActionVideoDetectionThread, self).__init__()
        self.logger = Logger().get_logger("ACTION_VIDEO_DETECTION_THREAD")

    def setPara(self, *args):
        self.type = args[0]["type"]
        self.COI = args[0]["COI"]
        self.dict = args[0]

    def setViolenceStop(self):
        self.stopCode = 1

    def initializeYolo(self):
        # TODO 条件控制
        score_thre = 0.3
        iou_thre = 0.3
        Database.yoloModel = YOLO(model_path=Database.modelPath,
                                  classes_path=Database.classes_path,
                                  weights_only=True,
                                  score=score_thre,
                                  iou=iou_thre)  # coco version

    def run(self) -> None:
        try:
            # 从数据库获取模型
            yolo = Database.yoloModel
            if isinstance(yolo, property):  # 模型不存在，初始化并存入数据库
                # 提示等待模型加载
                self._sendInfo("V", "检测到当前为初次使用，需要预加载模型以提高速度，后续将不再需要加载，请耐心等待片刻")
                self._sendInfo("T", "检测到当前为初次使用，需要预加载模型\n以提高速度，后续将不再需要加载。")
                self.initializeYolo()
                yolo = Database.yoloModel
            self._sendInfo("V", "模型加载完成，视频检测中")
            self.videoDetection(yolo)
            self._sendInfo("V", "视频检测结束")
            self._sendInfo("T", "视频检测结束")
            # 结束，发送终止信号
            self.overEmit.emit()

        except Exception as e:
            self._sendInfo("E", e.__str__())

    def videoDetection(self, yolo):
        self._sendInfo("I", "视频检测中.....")
        self.track_video(yolo=yolo, video_handle=self.dict["path"], camParamPath=self.dict["camParamPath"],
                         COI=self.COI, det_only=self.dict["onlyDect"],
                         writeVideo_flag=self.dict["avi"], dis_thre=self.dict["dis_thre"],
                         speed_thre=self.dict["speed_thre"])
        # 还原视频检测状态
        self._sendInfo("videoDetecting", None)
        # 写入结果
        (dir, videoName) = os.path.split(self.dict["path"])
        videoName = videoName.split(".")[0]
        with open(Database.workspace + "/" + videoName + "_车辆超速违章报告.txt", "w+") as f:
            f.write("          ======== 超速违章车辆检测报告 ======== \n      @Copyright by: JoeyforJoy,WHU222huan,GanAHE \n\n")
            for i in range(len(self.reportLine)):
                f.write(self.reportLine[i] + "\n")
        f.close()

    def streamDetection(self):
        # TODO 流视频
        pass

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

    def track_video(self, yolo, video_handle, camParamPath,
                    det_only=False, writeVideo_flag=False, COI=None,
                    dis_thre=60, speed_thre=6):
        """
        Track objects in a video
        :param yolo: a class define YOLO algorithm
        :param video_handle: 0 or video path
        :param camParamPath: 相机参数
        :param det_only: Bool
                if det_only==True, 只检测不跟踪
        :param writeVideo_flag: Bool 是否输出结果
        :param COI: list[str] -> 要识别的类别
        :param dis_thre: float -> 距离阈值。由于距离相机越远，测得的速度越不准确，超出这一距离，速度的测量值便不再可靠
        :param speed_thre: float -> 速度阈值。超出则超速
        :return: None
        """
        # read camera Parameters

        P = load_P(camParamPath)
        # create feature encoder
        model_filename = "./source/model/mars-small128.pb"
        encoder = gdet.create_box_encoder(model_filename, batch_size=1)

        video_capture = cv2.VideoCapture(video_handle)
        video_fps = int(video_capture.get(5))
        # create tracker
        tracker = Tracker(metric_mode="cosine", max_cosine_distance=0.3,
                          lambda0=1, nn_budget=None, buffer=video_fps)

        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fontsize = w//100
        thickness = w//300

        if writeVideo_flag:
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # 保存目标
            (dir, videoName) = os.path.split(video_handle)
            videoName = videoName.split(".")[0]
            out = cv2.VideoWriter(Database.workspace + "/" + videoName + "_Detection.avi", fourcc, 15, (w, h))
            list_file = open(Database.workspace + "/" + videoName + "_Detection.txt", 'w')
            frame_index = -1

        # 设置参数
        count = 1  # 当前帧数
        fps = 0.0
        time_gap = 10  # 10s 统计一次车流量
        traffic_flow = None  # 车流量 vec/h
        countor0 = 0  # 前一时刻的车流量
        time0 = 0  # 上次统计时的时间
        min_speed = 3  # 速度低于 min_speed km/h ，则设速度为0

        overspeed_tracks = {}

        self._sendInfo("I", "\n --首次(时间s)检测到超速违章情况：")
        # 状态信息栏初始化
        head = " " + '{0:{1}<8}\t'.format("时间(s)", " ") + \
               '{0:{1}<8}\t'.format("车辆ID", " ") + \
               '{0:{1}<12}\t'.format("车速(km/h)", " ") + \
               '{0:{1}<15}\t'.format("超速车辆牌号", " ")
        self._sendInfo("I", head)

        while True:
            # 检测终止标记
            if self.stopCode != 1:
                ret, frame = video_capture.read()  # frame shape 640*480*3
                if ret != True:
                    break
                t1 = time.time()

                """ ============= 目标检测与跟踪 =============="""

                # detect object
                image = Image.fromarray(frame[..., ::-1])  # bgr to rgb,CV to PIL
                img_show = Image.fromarray(frame[..., ::-1])

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
                detections = [Detection(bbox, score, class_, feature, frame=count)
                              for bbox, score, class_, feature in zip(boxes, scores, classes, features)]

                # Call the tracker
                tracker.predict()
                tracker.update(detections)

                """ ============= 车速估计、车牌号识别与实时信息显示 =============="""
                # detect only, not to track
                if det_only:
                    for bbox, score, cat in zip(boxes, scores, classes):
                        color = yolo.colors[yolo.class_names.index(cat)]
                        bbox = np.array(bbox)
                        bbox[2:] = bbox[:2] + bbox[2:]  # tlwh to tlbr
                        img_show = draw_detection_box(img_show, bbox, score, cat, color, fontsize)
                else:
                    for i, track in enumerate(tracker.tracks):
                        if not track.is_confirmed() or track.time_since_update > 1:
                            continue

                        # 车牌号识别
                        bbox = track.to_tlwh()
                        bbox = bbox.astype("int32")

                        license_plates, plate_scores, plate_boxes = lprBasedYOLO(image, [bbox], [track.object_class])
                        if len(license_plates) != 0:
                            track.license_plate_array.append(license_plates[0])
                            label = "%s\n%.3f" % (track.get_license_plate(), plate_scores[0])
                            img_show = draw_box(img_show, plate_boxes[0], label, (255, 0, 0), 
                                                fontsize=fontsize, thickness=thickness)

                        # 计算车速
                        if track.age % 5 == 0:
                            v, X, Y = computeObjectVelocity(track.box_array, P, track.frame_array, fps=video_fps)
                            mean_v = np.mean(v) * 3.6  # 取10帧内的平均速度(km/h)

                            # 当速度太小时，认为目标静止
                            if mean_v < min_speed:
                                mean_v = 0
                            # 存入跟踪器
                            track.speed = mean_v

                            # 计算距离
                            track.distance = np.mean(np.sqrt(X ** 2 + Y ** 2))

                        label = ""
                        if track.object_class in ["car", "truck", "bus"]:
                            label = "No.%d %s\nspeed: %3.f km/h\nplate: %s" % (track.track_id,
                                                                               track.object_class, track.speed,
                                                                               track.get_license_plate())
                        else:
                            label = "No.%d %s\nspeed: %3.f km/h" % (track.track_id, track.object_class, track.speed)

                        # 判断运动状态
                        state = judgeState(track.distance, track.speed, dis_thre, speed_thre)
                        track.motionState = state

                        bbox = track.to_tlbr()
                        img_show = draw_box(img_show, bbox, label,
                                         color=yolo.colors[yolo.class_names.index(track.object_class)],
                                         fontsize=fontsize, thickness=thickness, state=state)

                        # 保存超速车辆的信息
                        if state == MotionState.Overspeed:
                            if track.track_id in overspeed_tracks:
                                overspeed_tracks[track.track_id].setInfo(count, track.speed, track.get_license_plate())
                                if len(overspeed_tracks[track.track_id].frame_array) == 5:
                                    # 输出首次出现时的信息
                                    reStr = " " + '{0:{1}<10}\t'.format(str(count / video_fps), " ") + \
                                            '{0:{1}<8}\t'.format(str(track.track_id), " ") + \
                                            '{0:{1}<12.0f}\t'.format(track.speed, " ") + \
                                            '{0:{1}<15}\t'.format(track.get_license_plate(), " ")
                                    self._sendInfo("I", reStr)
                            else:
                                overspeed_tracks[track.track_id] = OverspeedTrack(track.track_id, count, track.speed,
                                                                                  track.get_license_plate())

                """ ============= 流量统计 =============="""
                # 计算车流量
                if count == video_fps:  # 最初的车辆数
                    countor0 = sum([v for v in tracker.category_countor.values()])
                    time0 = count / video_fps

                if (count != video_fps * time_gap) and (count % (video_fps * time_gap) == 0):
                    countor = sum([v for v in tracker.category_countor.values()])
                    traffic_flow = float(countor - countor0) / ((count / video_fps - time0) / 3600)
                    countor0 = countor
                    time0 = count / video_fps

                if traffic_flow is not None:
                    img_show = add_text(img_show, "traffic flow : %.0f vec/h" % traffic_flow,
                                     [20, 20], fontsize=fontsize*2, font_color=(255, 255, 0))

                # 计数
                cat_countor = ""
                for key, val in tracker.category_countor.items():
                    cat_countor += key + " : " + str(val) + "\n"
                img_show = add_text(img_show, cat_countor, [20, 60], fontsize=fontsize*2, font_color=(0, 255, 255))

                """ ============= 输出结果 =============="""
                # 加入队列并发送已完成信号
                self.queue.imageStrak(img_show)
                self._sendInfo("M", None)

                # output result
                if writeVideo_flag:
                    # save each frame
                    frame_name = "%06d" % count
                    # cv2.imwrite("./MTD/output/img1/" + frame_name, frame)

                    img_show = np.asarray(img_show)[...,::-1]
                    out.write(img_show)  # 存入视频
                    frame_index = frame_index + 1

                    for track in tracker.tracks:
                        list_file.write(frame_name + ',')  # frane_id
                        list_file.write(str(track.track_id) + ",")
                        bbox = track.to_tlwh()
                        list_file.write((str(bbox[0]) + "," + str(bbox[1]) + "," +
                                         str(bbox[2]) + "," + str(bbox[3]) + ","))
                        list_file.write(str(track.confidence * 100) + ",")
                        list_file.write("-1,-1,-1,")
                        list_file.write(track.object_class)
                        list_file.write('\n')

                # 超速数据输出到界面
                # if len(tracker.tracks) > 0:  # 取当前的值，也就是最后一位
                #     if tracker.tracks[-1].speed >= speed_thre:
                #         reStr = " " + '{0:{1}<6}\t'.format(str(ID) + "-" + str(tracker.tracks[-1].track_id), " ") + \
                #                 '{0:{1}<5}\t'.format(str(tracker.tracks[-1].frame_array[-1]), " ") + \
                #                 '{0:{1}<15}\t'.format(str(round(tracker.tracks[-1].speed, 5)), " ") + \
                #                 '{0:{1}<15}\t'.format(str(tracker.tracks[-1].get_license_plate()), " ")
                #         self._sendInfo("I", reStr)
                #         ID += 1

                # lens = len(tracker.tracks) - 1

                count += 1
                fps = (fps + (1. / (time.time() - t1))) / 2
                self._sendInfo("F", str(fps))

            else:
                self._sendInfo("I", "退出检测中...")
                # 有终止标记，退出循环，同时将标记恢复初始化
                self.stopCode = 0
                break

        """========= 输出总的超速车辆信息 =========="""
        self._sendInfo("I", "\n=====超速车辆统计======")
        head = " " + '{0:{1}<7}\t'.format("车辆ID", " ") + \
               '{0:{1}<16}\t'.format("出现时段(s)", " ") + \
               '{0:{1}<16}\t'.format("最大车速(km/h)", " ") + \
               '{0:{1}<16}\t'.format("超速车辆牌号", " ")
        self._sendInfo("I", head)
        self.reportLine.append(head)

        for id, info in overspeed_tracks.items():
            reStr = " " + '{0:{1}<7}\t'.format(str(id), " ") + \
                    '{0:{1}<16}\t'.format(str(round(info.frame_array[0] / video_fps, 3)) + str(' ~ ')
                                          + str(round(info.frame_array[-1] / video_fps, 3)), " ") + \
                    '{0:{1}<16.0f}\t'.format(max(info.speed_array), " ") + \
                    '{0:{1}<16}\t'.format(info.get_license_plate(), " ")
            self._sendInfo("I", reStr)
            self.reportLine.append(reStr)

        video_capture.release()
        if writeVideo_flag:
            out.release()
            list_file.close()
        cv2.destroyAllWindows()

    def streamVideo(self):
        """
        在线视频/监控视频流检测
        :return:
        """
        pass
