#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

"""
comment:数据处理集合

@author: GanAH  2019/9/27.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import sys
from PyQt5 import QtWidgets

class DataFilter(object):
    app = QtWidgets.QApplication(sys.argv)
    textArea = QtWidgets.QTextEdit()

    headEndSign = "END OF HEADER"
    def __init__(self,textArea):
        
        self.textArea = textArea


    def staLocation(sourceArrayStrCoor):
        """
        单星历数据处理
        
        第一行为星历信息
        后七条为广播轨道
        :param sourceArrayStrCoor: 传入的未处理原始字符数据
        :return: para:已处理的结果数据
        """
        # 广播轨道数据存储
        filterResult = [[0] * 4 for da in range(7)]

        for i in range(8):
            PRN_time = [0, 0, 0, 0]
            rowData = [0, 0, 0, 0]
            # 如果为第一行星历数据
            if i == 0:
                print(re.split('[\s]', sourceArrayStrCoor[i].strip()))
                strPrn = re.split('[\s]', sourceArrayStrCoor[i].strip())
                PRN_time[0] = strPrn[0]
                PRN_time[1] = strPrn[9]
                PRN_time[2] = strPrn[10]
                PRN_time[3] = strPrn[11]
            # 广播轨道数据
            else:
                for j in range(4):
                    if j == 0:
                        rowData[j] = sourceArrayStrCoor[i][3:22]
                    else:
                        rowData[j] = sourceArrayStrCoor[i][(j - 1) * 19 + 22:j * 19 + 22]

            filterResult[i - 1] = rowData

            # 数据处理结果存入，循环i次，但第一次开始才是广播轨道数据
        return PRN_time, filterResult

    def twoMISstringToFloat(self, twoMISstrArray):
        """
        字符串数据转float型
        :return: float
        """
        # 获取长度
        arrayLen = len(twoMISstrArray)
        arraychildLen = len(twoMISstrArray[0])
        floatArray = [[0] * 4 for da in range(7)]
        # 开始转换
        for i in range(arrayLen):
            for j in range(arraychildLen):
                floatArray[i][j] = float(twoMISstrArray[i][j])

        return floatArray

    def igsDataFilter(self, listDatas):
        """
        IGS电离层数据清洗
        :param listData:list--data
        :return: dic-->headStr,list-->dayETC,
        """
        textArea = self.textArea
        """
        # 头文件处理体
        # 获取头文件结束位置（行号），传递给第二循环体：数据清洗体
        """
        # 限定参数
        listData = listDatas
        headLineEndIndex = 0
        for i in range(len(listData)):  # 划分文件
            presentLine = listData[i].strip()  # 逐行处理,除去字符串首前尾后的空格，字符串内部不计入
            if presentLine == self.headEndSign:
                headLineEndIndex = i
                break

        """
        # 采集数据清洗体
        
        #字典存储ETC
        :key:时间（hours）及组号
        :keyword:不同经度的TEC（-180~180°每隔5°采集）
        """
        start_etc_map = "STARTOFTECMAP"

        time_list_index = []
        TIME_LON_LAT_ETC = []
        for i in range(headLineEndIndex + 1, len(listData)):
            etc_map_line = listData[i].replace(" ", "")  # 去除所有的空格
            # print("测试："+etc_map_line)
            if (start_etc_map in etc_map_line) is True:
                """
                #不同时间分组处理头数据：组别listData【i】/时间listData【i+1】/及排序listData【i+2】
                #说明：years + months + days + hours + etc_list_number
                # i 为匹配的行号，从当前匹配的位置起算三行为预处理数据
                """
                # 分隔
                etc_list_number = listData[i].split()[0]
                textArea.append("\n匹配位置："+str(i)+ "对应序号：" + str(etc_list_number))
                timeList = listData[i + 1].split()
                textArea.append("时间戳："+str( timeList))
                child_head = timeList[0] + "-" + timeList[1] + "-" + timeList[2] + "-" + timeList[
                    3] + "-" + etc_list_number
                textArea.append(child_head)
                #去除时间列表无关信息
                timeList = list(timeList)
                for i in range(4):
                    '''
                    #循环pop的话，默认pop尾数(栈顶)
                    # 如按序号pop，需要注意每次pop后总长度已经减小
                    '''
                    timeList.pop()
                time_list_index.append(timeList)

                """
                # 确定组别范围后，内循环获取该组内数据
                # 开始位置：i+1 为 START OF TECMAP的下一个：采集数据处的经纬度-高程
                """
                end_etc_map = "ENDOFTECMAP"
                lat_lon_H = "LAT/LON1/LON2/DLON/H"
                list_ETC_lat_index = []
                list_ETC_lat_data = []

                for no in range(i + 2, len(listData)):  # 遇到start etc map,从i+2即每单元开始记录
                    list_end_control = listData[no].replace(" ", "")
                    if (lat_lon_H in list_end_control) is True: #遇头分划另类处理输出
                        textArea.append("---文件划分---")
                        textArea.append(str(etc_list_number)+ "组"+str( no)+ "行：："+ str(self.__lat_lon_etc(listData[no])))

                        # 删除说明注释LAT/LON1/LON2/DLON/H的纬度头文件并存入，重复13次，可优化
                        listPop = self.__lat_lon_etc(listData[no])
                        listPop.pop(5)
                        list_ETC_lat_index.append(listPop)

                        #内部小循环取相同纬度下不同经度数据
                        #
                        list_lat = []
                        for latRound in range(no+1,no+6):
                            datalist = listData[latRound].split()
                            for indexData in range(len(datalist)):
                                list_lat.append(datalist[indexData])
                        #加入总数组
                        TIME_LON_LAT_ETC.append(list_lat)

                        #完成,加入总数组
                        list_ETC_lat_data.append(list_lat)

                    elif(end_etc_map in list_end_control) is True: #遇尾不输出，跳出当前小循环
                        textArea.append("时间切换，下一个采集时间：------------------")
                        break
                    else:
                        textArea.append(str(etc_list_number)+ "组"+str( no)+"行：："+str(listData[no].split()))







            """
            # 文件循环结束，外循环退出
            # 标志：ENDOFFILE
            """
            end_of_file = "ENDOFFILE"
            if (end_of_file in etc_map_line) is True:
                textArea.append("\n文件清洗结束！！！！！！！！！！！\n")
                break

        textArea.append("\n===========最终结果：==========")
        # print("  时间：",time_list_index)
        # print("经纬度：", list_ETC_lat_index)
        # print("三维数据：",TIME_LON_LAT_ETC)
        # print("长度：",len(TIME_LON_LAT_ETC),len(TIME_LON_LAT_ETC[0]))


        #返回清洗的数据结果
        return time_list_index,list_ETC_lat_index,TIME_LON_LAT_ETC

    def __lat_lon_etc(self, list_lat_lon):
        """
        将不同经度的ETC分隔返回

        :param list_lat_lon:单纬度数据 str
         <p>-87.5-180.0 180.0   5.0 450.0        LAT/LON1/LON2/DLON/H

        :return:单行分隔数据结果
        """
        splitLAT_LON = [0, 0, 0, 0, 0,0]  # 13*5
        for i in range(5):
            if i == 0:
                splitLAT_LON[i] = list_lat_lon[0:8]
            else:
                splitLAT_LON[i] = list_lat_lon[(i - 1) * 6 + 8:i * 6 + 8]
        splitLAT_LON[5] = "LAT/LON1/LON2/DLON/H"
        return splitLAT_LON
