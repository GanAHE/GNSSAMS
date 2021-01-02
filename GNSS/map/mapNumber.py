#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 地图图幅编号

@author: GanAH  2019/12/8.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""


def map_number(strMapCode, Lon, Lat):
    """
    单位： °
    """
    longitudeDF = {"A": 6 * 3600, "B": 3 * 3600, "C": 1 * 3600 + 30 * 60, "D": 30 * 60, "E": 15 * 60, "F": 7 * 60 + 30,
                   "G": 3 * 60 + 45, "H": 1 * 60 + 52.5}
    latitudeDF = {"A": 4 * 3600, "B": 2 * 3600, "C": 1 * 3600, "D": 20 * 60, "E": 10 * 60, "F": 5 * 60,
                  "G": 2 * 60 + 30, "H": 1 * 60 + 15}
    mapCode = {"A": "1：100万", "B": "1：50万", "C": "1：25万", "D": "1：10万", "E": "1：5万", "F": "1：2.5万", "G": "1：1万",
               "H": "1：5000", }
    try:
        if ord(strMapCode) >= 65 and ord(strMapCode) <= 72:
            row1 = int(Lat / 4) + 1
            column1 = int(Lon / 6) + 31
            if strMapCode == "A":
                return mapCode[strMapCode] + "地图分幅代号 :" + chr(row1 + 64).strip() + str(column1).rjust(2, '0')
            else:
                row2 = int(4 * 3600 / latitudeDF[strMapCode]) - int((Lat % 4) * 3600 / latitudeDF[strMapCode])
                column2 = int((Lon % 6) * 3600 / longitudeDF[strMapCode]) + 1
                return mapCode[strMapCode] + "地图分幅代号 :" + chr(row1 + 64).strip() + str(column1).rjust(2,
                                                                                                      '0') + strMapCode + str(
                    row2).rjust(3, '0') + str(column2).rjust(3,
                                                             '0')
        else:
            print("地图图幅编号等级错误！")
            return None

    except Exception as e:
        print("Error! the infomation like these:")
        print(e.__str__())
        return None


a = 114.5625
b = 39.375
print("Lon:" + str(a) + " , lat:" + str(b))
for i in range(8):
    print(map_number(chr(i + 65), a, b))
