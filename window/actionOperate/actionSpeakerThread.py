#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 语音朗读模块

@author: GanAH  2020/6/17.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

import pythoncom
import win32com.client
from PyQt5.QtCore import pyqtSignal, QThread

from database.database import Database
from loggerConfig.logger import Logger


class SpeakerThread(QThread):
    infoEmit = pyqtSignal(str, str)

    def __init__(self):
        super(SpeakerThread, self).__init__()
        self.logger = Logger().get_logger("ACTION_SPEAKER_THREAD")

    def setText(self, text):
        self.text = text

    def run(self) -> None:
        self.speak()

    def speak(self):
        try:
            # 从数据库查看是否开启该功能
            enable = Database.speaker
            if enable:
                self.logger.info("语音播报：" + self.text)
                pythoncom.CoInitialize()
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                pythoncom.CoInitialize()
                speaker.Speak(self.text)
            # 线程休眠
            # self
        except Exception as e:
            print(e.__str__())
            self.infoEmit.emit("E", "1.意料之外的错误，位于：" + e.__str__() + "\n2.如此错误过于频繁，说明当前环境不支持该功能，\n请在系统系统设置中关闭语音功能。")

    def threadSleep(self):
        self.wait(20)
