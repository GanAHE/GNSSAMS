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
import multiprocessing
import numpy as np
from sklearn.cluster import Birch
import matplotlib.pyplot as plt


def video2frame(video_name):
    total_frames = []
    cap = cv2.VideoCapture(video_name)
    c = 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps is {}'.format(fps))
    if cap.isOpened() == False:
        print('Error opening video stream of file')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            if c == 1:
                total_frames.append(frame)
            elif c % int(fps) == 0:
                total_frames.append(frame)

        else:
            break
        c += 1
    cap.release()
    return total_frames


def calc_hist(frame):
    h, w, _ = frame.shape
    temp = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([temp], [0, 1, 2], None, [12, 5, 5], [0, 256, 0, 256, 0, 256])
    hist = hist.flatten()
    hist /= h * w
    return hist


def similarity(a1, a2):
    ## compute similarity between frames.
    # temp = np.concatenate((a1,a2),axis=1)
    temp = np.vstack((a1, a2))
    # print(temp)
    # print(temp.shape)
    s = temp.min(axis=0)
    # print(s.shape)
    si = np.sum(s)
    # print(si)
    return si


def ekf(total_frames):
    ## extract key frames from total frames.
    ## First cluster.
    ## Second ekf.
    centers_d = {}
    result = []
    for i in range(len(total_frames)):
        temp = 0.0
        if len(centers_d) < 1:
            centers_d[i] = [total_frames[i], i]
        else:
            centers = list(centers_d.keys())
            for index, each in enumerate(centers):
                ind = -1
                t_si = similarity(total_frames[i], centers_d[each][0])
                # print(t_si)
                if t_si < 0.8:
                    continue
                elif t_si > temp:
                    temp = t_si
                    ind = index
                else:
                    continue
            if temp > 0.8 and ind != -1:
                centers_d[centers[ind]].append(i)
                length = len(centers_d[centers[ind]]) - 1
                c_old = centers_d[centers[ind]][0] * length
                c_new = (c_old + total_frames[i]) / (length + 1)
                centers_d[centers[ind]][0] = c_new
            else:
                centers_d[i] = [total_frames[i], i]

    cks = list(centers_d.keys())
    for index, each in enumerate(cks):
        if len(centers_d[each]) <= 6:
            result.extend(centers_d[each][1:])
        else:
            temp = []
            accordence = {}
            c = centers_d[each][0]
            for jindex, jeach in enumerate(centers_d[each][1:]):
                accordence[jindex] = jeach

                tempsi = similarity(c, total_frames[jeach])
                temp.append(tempsi)
            oktemp = np.argsort(temp).tolist()
            print('oktemp {}'.format(oktemp))
            print('accordence: {}'.format(accordence))
            for i in range(5):
                oktemp[i] = accordence[oktemp[i]]

            result.extend(oktemp[:5])
    return centers_d, sorted(result)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=10)
    video_name = r'E:\CodePrograme\Python\EMACS\workspace\3Dimess\stack\VID_20200918_181432.mp4'
    total_frames = video2frame(video_name)
    print("there are {} frames in video".format(len(total_frames)))
    h, w, _ = total_frames[0].shape
    hist = pool.map(calc_hist, total_frames)
    print('hist.shape: {}'.format(hist[0].shape))
    # print('hist[0]: {}'.format(hist[0]))

    si = similarity(hist[50], hist[60])
    print('similarity between two frames: {}'.format(si))
    # print((hist[1]+hist[2]+hist[3])/3)
    cents, results = ekf(hist)
    print(len(cents), results)
    # to_show = cv2.cvtColor(total_frames[cents[0][-1]], cv2.COLOR_BGR2RGB)
    # plt.imshow(to_show)
    # plt.show()
    print(type(total_frames[0]))
    k = 0
    for inm in total_frames:
        print("关键帧提取中:" + str(k + 1))
        to_show = cv2.cvtColor(total_frames[k], cv2.COLOR_BGR2RGB)
        plt.imsave("E:\\CodePrograme\\Python\\EMACS\\geodeticSurvey\\mvs\\te\\Gr_"+ str(k)+".jpg",to_show)
        # plt.imshow(to_show)
        # plt.show()
        # inm.save("./te/" + str(k) + ".jpg")
        # cv2.imwrite("./te/" + str(k) + ".jpg", inm)
        k += 1
