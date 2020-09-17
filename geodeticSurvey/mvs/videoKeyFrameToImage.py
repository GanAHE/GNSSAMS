#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
project: EMACS
comment: 

@author: GanAHE  2020/9/15.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import cv2
import numpy as np
import os

# Playing video from file:
#mp4 video location

def getVideoKeyFrame(videoPath,frameSaveDir):
    """
    提取视频关键帧
    针对视频类型的三维建模
    :param videoPath:
    :param frameSaveDir:
    :return:
    """

    cap = cv2.VideoCapture(videoPath)

    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    currentFrame = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Saves image of the current frame in jpg file
        name = './data/frame' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        currentFrame += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

