#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
project: EMACS
comment: 

@author: GanAHE  2020/9/15.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


def save_bundle_rd_out(structure, K, rotations, motions, colors, correspond_struct_idxs, keypoints_for_all):
    """
    导出SFM成果
    :param structure:
    :param K:
    :param rotations:
    :param motions:
    :param colors:
    :param correspond_struct_idxs:
    :param keypoints_for_all:
    :return:
    """
    header = "# Bundle file v0.3"
    num_camera = len(rotations)
    num_point = len(structure)
    with open("./source/exModule/VMCS/pmvs/bundle.rd.out", "w") as f:
        # write header and two number
        f.write(header + "\n")
        f.write(str(num_camera) + " " + str(num_point) + "\n")

        # write cameras
        # 第一行：焦距f 畸变参数k1 畸变参数k2
        # 第二到四行：旋转矩阵R
        # 第五行：平移量t
        for i in range(num_camera):
            focal_length = 0.5 * (K[0][0] + K[1][1])
            R = rotations[i]
            T = motions[i]
            f.write(str(focal_length) + " 0 0\r"
                    + str(R[0][0]) + " " + str(R[0][1]) + " " + str(R[0][2]) + "\r"
                    + str(R[1][0]) + " " + str(R[1][1]) + " " + str(R[1][2]) + "\r"
                    + str(R[2][0]) + " " + str(R[2][1]) + " " + str(R[2][2]) + "\r"
                    + str(T[0][0]) + " " + str(T[1][0]) + " " + str(T[2][0]) + "\r")

        # write points
        # 第一行：三维点的坐标
        # 第二行：该点的RGB颜色
        # 第三行：该点的详细信息
        for i in range(num_point):
            f.write(str(structure[i][0]) + " " + str(structure[i][1]) + " " + str(structure[i][2]) + "\n"
                    + str(colors[i][0]) + " " + str(colors[i][1]) + " " + str(colors[i][2]) + "\n")

            # get detailed information of points
            # 1. the number of cameras in which can observe the point
            # 2. the corresponding information about projection points of the point in images  camera index, keypoint index, x/y coordinante
            count = 0  # counter the number of camera
            info = ""
            for a in range(len(correspond_struct_idxs)):
                for b in range(len(correspond_struct_idxs[a])):
                    if correspond_struct_idxs[a][b] == i:
                        count += 1
                        info = info + str(a) + " "
                        info = info + str(b) + " "
                        info = info + str(keypoints_for_all[a][b].pt[0]) + " " + str(
                            keypoints_for_all[a][b].pt[1]) + " "
                        break

            f.write(str(count) + " " + info + "\n")
