#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 内存中转数据库
<p>持久化常量/变量保存区
@author: GanAH  2020/6/4.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import json


class Database(object):
    """
    # 模型相关配置，载入方式为：类名.属性 Ex: Database.modelPath
    # 上述操作需要预先对Database进行初始化，由软件启动时完成
    # 如需测试，载入方式为：实例化类.属性 ,Ex: Database().loadJsonConfig,Database.modelPath
    """
    jsonPath = "./source/para_json/config.json"
    modelPath = None
    default_modelPath = None
    font = None
    camParamPath = None
    default_camParamPath = None
    classes_path = None
    model_filename = None
    anchors_path = None
    workspace = None
    default_workspace = None
    envir = "CPU"
    default_envir = "CPU"
    speaker = 0
    default_speaker = 0
    LicensePath = None
    videoDetecting = False  # 视频检测状态：是否在执行

    localHelpDocument = "./source/document/test.html"
    onlineHelpLink = "https://www.ganahe.top/archives/ITSMSHelp.html"

    welcomeSpeak = "欢迎使用VLPRVTL目标检测软件，当前已开启语音解读功能，参数可在系统设置中调整，祝您使用愉快——小小搬运工开发组"

    def loadJsonConfig(self):
        """
        加载json配置文件
        :return: None
        """
        # 读取json文件内容,返回字典格式
        with open(self.jsonPath, 'r', encoding='utf8')as fp:
            # with open('../source/para_json/config.json', 'r', encoding='utf8')as fp:
            dict_data = json.load(fp)
        Database.modelPath = dict_data["model"]["modelPath"]
        Database.default_modelPath = dict_data["default_modelPath"]
        Database.font = dict_data["model"]["font"]
        Database.classes_path = dict_data["model"]["classes_path"]
        Database.model_filename = dict_data["model"]["model_filename"]
        Database.camParamPath = dict_data["model"]["camParamPath"]
        Database.default_camParamPath = dict_data["default_camParamPath"]
        Database.anchors_path = dict_data["model"]["anchors_path"]
        Database.workspace = dict_data["workspace"]
        Database.default_workspace = dict_data["default_workspace"]
        Database.envir = dict_data["envir"]
        Database.default_envir = dict_data["default_envir"]
        Database.speaker = dict_data["speaker"]
        Database.default_speaker = dict_data["default_speaker"]
        Database.LicensePath = dict_data["License"]

    def writeJsonKeyValue(self, key1, value, key2=None):
        """
        修改键值
        :param key1: 键
        :param value: 值
        :param key2: 内键 主键为model时
        :return:
        """
        try:
            with open(self.jsonPath, "r") as f:
                jsonData = json.load(f)
            f.close()
            if key1 == "model" and key2 != None:  # json内字典
                jsonData[key1][key2] = value
                with open(self.jsonPath, "w") as r:
                    json.dump(jsonData, r)
                return True
            elif key1 != "model" and key2 is None:
                jsonData[key1] = value
                with open(self.jsonPath, "w") as r2:
                    json.dump(jsonData, r2)
                return True
            else:
                return False
        except Exception as e:
            return e.__str__()

    """
    # 单张图像识别结果
    """

    @property
    def imageResult(self):
        return self._imageResult

    @imageResult.setter
    def imageResult(self, imageAndICO):
        self._imageResult = imageAndICO

    @property
    def imagesPathList(self):
        return self._imagesPathList

    @imagesPathList.setter
    def imagesPathList(self, pathList):
        self._imagesPathList = pathList

    # 待识别影像路径
    @property
    def videoPath(self):
        return self._videoPath

    @videoPath.setter
    def videoPath(self, videoPath):
        self._videoPath = videoPath

    # 模型存储
    @property
    def yoloModel(self):
        """
        获取yolo模型
        :return: yolo type
        """
        return self._yoloModel

    @yoloModel.setter
    def yoloModel(self, yolo):
        """
        设置yolo模型
        :param yolo: 一个yolo对象
        """
        self._yoloModel = yolo

    @property
    def overSpeedReportData(self):
        return self._InfoList

    @overSpeedReportData.setter
    def overSpeedReportData(self, reportList):
        self._InfoList = reportList
