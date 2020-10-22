#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 多图像/视频帧队列

@author: GanAH  2020/6/4.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from PyQt5.QtCore import QObject, pyqtSignal


class Queue(QObject):
    queueEmit = pyqtSignal()
    _imageStrak = []
    _COI = []

    def imageStrak(self, image):
        self._imageStrak.append(image)

    def getImageStrak(self):
        if len(self._imageStrak) != 0:
            # 队列挤出
            return self._imageStrak.pop(0)
        else:
            return None

    def setImageCOI(self, COIDict):
        self._COI.append(COIDict)

    def getImageCOI(self):
        if len(self._COI) != 0:
            # 队列挤出
            return self._COI.pop(0)
        else:
            return None
