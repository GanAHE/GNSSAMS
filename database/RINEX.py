#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:RINEX文件处理类

@author: GanAH  2019/10/29.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
from GNSS.time.timeSystem import TimeSystemChange
from window.file.operationFile import OperationFile
from database.database import Database

from myConfig.logger import Logger

logger = Logger().get_logger("RINEX_FILE_ANALYSE")  # 日志信息


class RINEX_N():
    """
    # N 文件
    """
    _RINEXData = None
    _typeOfFile = None
    _versionOfFile = None
    _headOfIndex = None

    def __init__(self, QTextEdit):
        self._RINEXData = QTextEdit
        # 获取文件类型
        self._versionOfFile = self.setVersion(QTextEdit[0])
        self._headOfIndex = self.setHeadIndex(QTextEdit)
        self._typeOfFile = self.setFileType(QTextEdit[0] + QTextEdit[1])
        # 设定文件状态
        self.setFileStatus()

    def setHeadIndex(self, satelliteFileData):
        """
        头文件结束标志

        :param satelliteFileData:
        :return:
        """
        i = 0
        while satelliteFileData[i].strip() != "END OF HEADER":
            i += 1
        return i

    def setVersion(self, infoLine):
        return infoLine.split()[0]

    def setFileType(self, typeInformationLine):
        line = typeInformationLine.split()
        for i in range(1, len(line)):
            # 字符串比较：is比较id值，==比较字符串内的value
            if line[i].lower() == "navigation":
                return "N"

            elif line[i].lower() == "nav":
                return "N"

            elif line[i].upper() == "OBSERVATION":
                return "O"
        # 以上未 return 时
        Database.warnExceptionText = "Error: No correct the type of File's information !"
        return "Error"

    """
    # 属性存取
    #
    # <p> 公共方法，可被继承
    """

    @property
    def fileData(self):
        return self._RINEXData

    @fileData.setter
    def fileData(self, rinexFile):
        self._RINEXData = rinexFile

    @property
    def headIndex(self):
        return self._headOfIndex

    @headIndex.setter
    def headIndex(self, newHeadIndex):
        self._headOfIndex = newHeadIndex

    @property
    def versionOfFile(self):
        return self._versionOfFile

    @versionOfFile.setter
    def versionOfFile(self, newVersion):
        self._versionOfFile = newVersion

    @property
    def typeFile(self):
        return self._typeOfFile

    @typeFile.setter
    def typeFile(self, newType):
        self._typeOfFile = newType

    """
    # 类数据操作方法
    #
    # 部分通用，可被继承直接使用，部分需要：@Overwrite
    """

    def get_time_epochData(self, GLTimeList):
        """
        获取GLTime的一组导航电文
        :param GLTimeList:
        :return:
        """
        timeChange = TimeSystemChange(float(GLTimeList[0]), float(GLTimeList[1]), float(GLTimeList[2]),
                                      float(GLTimeList[3]), float(GLTimeList[4]), float(GLTimeList[5]))
        JDIndex = timeChange.GL2JD()
        print("JD", JDIndex)

        strDataList = self._RINEXData
        headEndIndex = self._headOfIndex
        satelliteOrbet = []
        # 提取导航电文数据,每隔八个为一组
        for i in range(headEndIndex + 1, len(strDataList), 8):
            gltime, satelliteClockParam = self._time_match(strDataList[i])
            print(gltime)
            JDIndex2 = TimeSystemChange(float(gltime[0]), float(gltime[1]), float(gltime[2]), float(gltime[3]), 0,
                                        0).GL2JD()
            print(JDIndex2)
            if JDIndex == JDIndex2:
                for k in range(1, 8):
                    satelliteOrbet.append(self._N_file_line_fitler(strDataList[i + k]))
                print("第", i, "行数据提取：", satelliteOrbet)
                return satelliteOrbet

    def _time_match(self, gavTimeListLine):
        """
        时间配准
        :param gavTimeListLine:
        :return:
        """
        rinexVersion = self._versionOfFile
        GLTime = []
        satelliteClockParam = []
        if rinexVersion == "3.02":
            timeList = gavTimeListLine.split()
            GLTime = timeList[1:7]
            satelliteClockParam = timeList[7:10]
            return GLTime, satelliteClockParam

        elif rinexVersion == "2.11":
            for i in range(10):
                if i < 6:
                    if i == 1:
                        GLTime.append("20" + gavTimeListLine[i * 3:i * 3 + 3])
                    elif i > 1:
                        GLTime.append(gavTimeListLine[i * 3:i * 3 + 3])
                elif i == 6:
                    GLTime.append(gavTimeListLine[i * 3:i * 3 + 4])
                else:
                    satelliteClockParam.append(gavTimeListLine[(i - 7) * 19 + 22:(i - 6) * 19 + 22])

            return GLTime, satelliteClockParam
        else:
            return "Error ! the version of File is Not standard."

    def _N_file_line_fitler(self, strline):
        list_split = [2, 0, 2, 0]
        # 非标准长度
        if self._versionOfFile == "3.02":
            if len(strline) != 81:
                return list_split
            # 标准RINEX长度
            else:
                for i in range(len(list_split)):
                    if (i == 0):
                        list_split[i] = strline[3:23]
                    else:
                        list_split[i] = strline[(i - 1) * 19 + 23: i * 19 + 23]
                return list_split
        else:
            if len(strline) != 80:
                return list_split
            # 标准RINEX长度
            else:
                for i in range(len(list_split)):
                    if (i == 0):
                        list_split[i] = strline[3:22]
                    else:
                        list_split[i] = strline[(i - 1) * 19 + 22: i * 19 + 22]
                return list_split

    def get_orbetListData(self):
        """
        获取导航电文所有数据
        :return: PRN,时间以及卫星钟参数 : time_List ; 对应前面时间序列，每隔7行为一组 ：all_epoch_List 。
        """
        headIndex = self._headOfIndex
        controlNum = 0
        time_List = []
        all_epoch_List = []
        for i in range(headIndex + 1, len(self._RINEXData)):
            # print("单组行内号：：", controlNum, "行号：：", i)
            controlNum += 1
            # print("第{%d1}"%i,controlNum)

            if controlNum == 1:  # PRN,时间以及卫星钟参数
                time_List.append(self._RINEXData[i])
            elif controlNum > 1 and controlNum < 8:  # 下属的七条轨道数据
                # 提取单行数据转换
                line_orbet = self._N_file_line_fitler(self._RINEXData[i])
                #
                # print("行号：", controlNum, '长度：', len(self._RINEXData[i]), '\n待处理数据：', self._RINEXData[i], '划分后的数据：',
                #       line_orbet)

                floatData = [0, 0, 0, 0]
                # 字符转换为数据， + “0”保证空数据可转换
                for k in range(len(line_orbet)):
                    # print("划分的字符数据逐个转换,当前:", line_orbet[k].strip())
                    line_orbet[k] = self.stringFortranToData(line_orbet[k].strip())
                all_epoch_List.append(line_orbet)
                # print("\n_____________________")
            else:
                # 下一组初始化定位
                controlNum = 0
        return time_List, all_epoch_List

    def stringFortranToData(self, stringValue):
        """
        将Fortran类型的双精度实型字符转换为数据类型
        :param stringValue: 4.54565D45
        :return: float Data
        """
        # 当导航电文本行置空替代0，需要自行转替回来
        if stringValue == "":
            centerString = '0'
        else:
            centerString = stringValue
            for i in range(len(stringValue)):
                if stringValue[i] == 'D':
                    centerString = stringValue.replace("D", "E")

        return float(centerString)

    def getInformation(self):
        return [self._versionOfFile, self._typeOfFile, self._headOfIndex]

    def setFileStatus(self):
        """
        判断读入的文件是否正常，并存储结果
        :return: None
        """
        info_file = self.getInformation()
        for i in range(len(info_file)):
            pass
            # to do
            # 怎么判断？？
            exist = 1  # 在读入文件时设定
            status = 1
            if info_file[i] is None:
                status = 0
            Database.RINEX_status = exist, status


class RINEX_O(RINEX_N):
    """
    # O 文件
    """
    _startETCTime = [0, 0]
    _observerStation = None
    _manufacturer = None
    _antennaHeight = None
    _masureAntennaHeightWay = None
    _interval = None
    _observerStationNearPosition = [0, 0, 0]

    def __init__(self, observertionText):
        self.fileData = observertionText
        self.versionOfFile = self.setVersion(observertionText[0])
        self.headIndex = self.setHeadIndex(observertionText)
        self._typeOfFile = self.setFileType(observertionText[0] + observertionText[1])
        self._setObserverTionFileInfo()
        # 设定文件状态
        self.setFileStatus()

    def _setObserverTionFileInfo(self):
        """
        设定观测文件头文件信息

        :return: None
        """
        for i in range(self.headIndex):
            lineStr = self.fileData[i]
            lineInfo = lineStr.split()
            # 获取测站近似坐标
            if "APPROX POSITION XYZ" in lineStr:
                self._observerStationNearPosition = [lineInfo[0], lineInfo[1], lineInfo[2]]
            if "INTERVAL" in lineStr:
                self._interval = lineInfo[0]
            # 非共性问题
            if self._versionOfFile == "3.02":
                if "PGM / RUN BY / DATE" in lineStr:
                    self._manufacturer = lineInfo[0]
                if "MARKER NAME" in lineStr:
                    self._observerStation = lineInfo[0]
                if "ANTENNA: DELTA H/E/N" in lineStr:
                    self._antennaHeight = lineInfo[0]
                if "PGM / RUN BY / DATE" in lineStr:
                    self._startETCTime = [lineInfo[2], lineInfo[3]]
            if self._versionOfFile == "2.11":
                pass

    def get_time_epochData(self, GLTimeList):
        pass

    def get_satelliteObver_Info_list(self):
        """
        观测文件信息
        <p> 时间，字符信息,
        :return:
        """
        source_observe_list = []
        time_list = []
        if self.versionOfFile == "3.02":
            for i in range(self.headIndex + 1, len(self.fileData)):
                # 时间序列
                if self.fileData[i][0] == ">":
                    time_line_list = self.fileData[i].split()
                    # 去除头标识 ：“>”
                    del (time_line_list[0])
                    time_list.append(time_line_list)

                    pass
                # 对应时间下的观测数据
                else:
                    line_list = self.fileData[i].split()
                    # 固定list长度为13
                    while len(line_list) < 13:
                        line_list.append("0")
                    source_observe_list.append(line_list)

            return time_list, source_observe_list

        else:
            print("当前版本出错！")

        pass

    def getInformation(self):
        return (self.versionOfFile, self._typeOfFile, self._startETCTime, self.headIndex, self._antennaHeight,
                self._observerStation, self._interval, self._observerStationNearPosition, self._manufacturer)


class RINEX_C():
    pass


class RINEX_OHTER():
    pass


"""
#测试单元
"""

if __name__ == "__main__":
    fileName = ["brdc1710.10n", "GP008301I.19n", "D068305A.19N", "dav11710.10o", "GP008301I.19o", "D068305A.19O"]
    # testFile_N = fileName[0]
    # dataList = operationFile().readlargeFile("../source/" + testFile_N)
    # print("———测试N文件------" + testFile_N)
    # a = RINEX_N(QTextEdit = dataList)
    # print(a.getInformation())
    # line = a.get_all_orbetListData()
    # print("---------------------全数据！---------------------")
    # for i in range(len(line)):
    #     print(line[i])

    data = OperationFile().readlargeFile("../source/" + fileName[5])
    logger.info("---测试O文件---")
    logger.debug("测试日志")
    b = RINEX_O(data)
    print("B", b.headIndex)
    logger.info("输出信息")
    print(b.getInformation())
    logger.info("获取文件状态信息")
    print(Database.RINEX_status)
