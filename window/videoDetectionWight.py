# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videoDetectionWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import os

from PIL.Image import fromqpixmap
from PyQt5 import QtCore, QtGui, QtWidgets

from MTD.deep_sort.track import Track
from MTD.deep_sort.tracker import Tracker
from database.database import Database
from database.imageQueue import Queue
from window.actionOperate.actionPicturesDetectionThread import ActionPicturesDetectionThread
from window.actionOperate.actionVideoDetectionThread import ActionVideoDetectionThread
from window.tipDig import ActionWarnException


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)
    count = 0
    frameCount = 1

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1219, 704)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(350, 700))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setMouseTracking(False)
        self.groupBox.setTabletTracking(False)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_person = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_person.setObjectName("checkBox_person")
        self.horizontalLayout_5.addWidget(self.checkBox_person)
        self.checkBox_bicycle = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_bicycle.setObjectName("checkBox_bicycle")
        self.horizontalLayout_5.addWidget(self.checkBox_bicycle)
        self.checkBox_car = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_car.setObjectName("checkBox_car")
        self.horizontalLayout_5.addWidget(self.checkBox_car)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBox_truck = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_truck.setObjectName("checkBox_truck")
        self.horizontalLayout_7.addWidget(self.checkBox_truck)
        self.checkBox_bus = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_bus.setObjectName("checkBox_bus")
        self.horizontalLayout_7.addWidget(self.checkBox_bus)
        self.checkBox_train = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_train.setObjectName("checkBox_train")
        self.horizontalLayout_7.addWidget(self.checkBox_train)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.radioButton_selectAll = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_selectAll.setObjectName("radioButton_selectAll")
        self.horizontalLayout_10.addWidget(self.radioButton_selectAll)
        self.radioButton_noSelect = QtWidgets.QRadioButton(self.groupBox_6)
        self.radioButton_noSelect.setObjectName("radioButton_noSelect")
        self.horizontalLayout_10.addWidget(self.radioButton_noSelect)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6.addWidget(self.groupBox_6)
        self.verticalLayout_11.addWidget(self.groupBox_5)
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.checkBox_saveFrame = QtWidgets.QCheckBox(self.tabWidgetPage2)
        self.checkBox_saveFrame.setObjectName("checkBox_saveFrame")
        self.verticalLayout_10.addWidget(self.checkBox_saveFrame)
        self.checkBox_saveAVI = QtWidgets.QCheckBox(self.tabWidgetPage2)
        self.checkBox_saveAVI.setObjectName("checkBox_saveAVI")
        self.verticalLayout_10.addWidget(self.checkBox_saveAVI)
        self.checkBox_onlyDect = QtWidgets.QCheckBox(self.tabWidgetPage2)
        self.checkBox_onlyDect.setObjectName("checkBox_onlyDect")
        self.verticalLayout_10.addWidget(self.checkBox_onlyDect)
        self.line_3 = QtWidgets.QFrame(self.tabWidgetPage2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_10.addWidget(self.line_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_start = QtWidgets.QPushButton(self.tabWidgetPage2)
        self.button_start.setObjectName("button_start")
        self.horizontalLayout_2.addWidget(self.button_start)
        self.button_over = QtWidgets.QPushButton(self.tabWidgetPage2)
        self.button_over.setObjectName("button_over")
        self.horizontalLayout_2.addWidget(self.button_over)
        self.verticalLayout_10.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.tabWidgetPage2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_10.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.tabWidgetPage2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_12.addWidget(self.label_3)
        self.dial = QtWidgets.QDial(self.tabWidgetPage2)
        self.dial.setSingleStep(1)
        self.dial.setWrapping(True)
        self.dial.setNotchesVisible(False)
        self.dial.setMaximum(150)
        self.dial.setObjectName("dial")
        self.horizontalLayout_12.addWidget(self.dial)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_7 = QtWidgets.QLabel(self.tabWidgetPage2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_13.addWidget(self.label_7)
        self.spinBox_speed = QtWidgets.QDoubleSpinBox(self.tabWidgetPage2)
        self.spinBox_speed.setMaximum(150.0)
        self.spinBox_speed.setSingleStep(5.0)
        self.spinBox_speed.setProperty("value", 60.0)
        self.spinBox_speed.setObjectName("spinBox_speed")
        self.horizontalLayout_13.addWidget(self.spinBox_speed)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_8 = QtWidgets.QLabel(self.tabWidgetPage2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_14.addWidget(self.label_8)
        self.spinBox_distance = QtWidgets.QDoubleSpinBox(self.tabWidgetPage2)
        self.spinBox_distance.setMaximum(200.0)
        self.spinBox_distance.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.spinBox_distance.setProperty("value", 60.0)
        self.spinBox_distance.setObjectName("spinBox_distance")
        self.horizontalLayout_14.addWidget(self.spinBox_distance)
        self.verticalLayout_2.addLayout(self.horizontalLayout_14)
        self.groupBox_7 = QtWidgets.QGroupBox(self.tabWidgetPage2)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox_7)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_15.addWidget(self.lcdNumber)
        self.verticalLayout_9.addLayout(self.horizontalLayout_15)
        self.verticalLayout_2.addWidget(self.groupBox_7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.tabWidgetPage2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_10.addWidget(self.line_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/bance.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabWidgetPage2, icon, "")
        self.tabWidgetPage3 = QtWidgets.QWidget()
        self.tabWidgetPage3.setObjectName("tabWidgetPage3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tabWidgetPage3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBox_autoSaveImage = QtWidgets.QCheckBox(self.tabWidgetPage3)
        self.checkBox_autoSaveImage.setObjectName("checkBox_autoSaveImage")
        self.verticalLayout_7.addWidget(self.checkBox_autoSaveImage)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_2 = QtWidgets.QLabel(self.tabWidgetPage3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_11.addWidget(self.label_2)
        self.comboBox_mode = QtWidgets.QComboBox(self.tabWidgetPage3)
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.horizontalLayout_11.addWidget(self.comboBox_mode)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.line_5 = QtWidgets.QFrame(self.tabWidgetPage3)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_7.addWidget(self.line_5)
        self.radioButton_tipShowImages = QtWidgets.QRadioButton(self.tabWidgetPage3)
        self.radioButton_tipShowImages.setObjectName("radioButton_tipShowImages")
        self.verticalLayout_7.addWidget(self.radioButton_tipShowImages)
        self.radioButton_showImages = QtWidgets.QRadioButton(self.tabWidgetPage3)
        self.radioButton_showImages.setObjectName("radioButton_showImages")
        self.verticalLayout_7.addWidget(self.radioButton_showImages)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.line_4 = QtWidgets.QFrame(self.tabWidgetPage3)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_8.addWidget(self.line_4)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tabWidgetPage3)
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.button_imagePath = QtWidgets.QPushButton(self.groupBox_3)
        self.button_imagePath.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./source/icon/more.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_imagePath.setIcon(icon1)
        self.button_imagePath.setObjectName("button_imagePath")
        self.horizontalLayout_6.addWidget(self.button_imagePath)
        self.horizontalLayout_9.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tabWidgetPage3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.button_imagePath_2 = QtWidgets.QPushButton(self.groupBox_4)
        self.button_imagePath_2.setText("")
        self.button_imagePath_2.setIcon(icon1)
        self.button_imagePath_2.setObjectName("button_imagePath_2")
        self.horizontalLayout_8.addWidget(self.button_imagePath_2)
        self.horizontalLayout_9.addWidget(self.groupBox_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./source/icon/hore.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabWidgetPage3, icon2, "")
        self.verticalLayout_11.addWidget(self.tabWidget)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setStyleSheet("background-color: rgb(242, 251, 255);")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("./source/icon/icon_any.png"))
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_image = QtWidgets.QLabel(self.groupBox_2)
        self.label_image.setText("")
        self.label_image.setPixmap(QtGui.QPixmap("./source/icon/animation.png"))
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName("label_image")
        self.verticalLayout_4.addWidget(self.label_image)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)

        self.button_start.clicked.connect(self.dectVideo)
        self.button_over.clicked.connect(self.violenceStop)
        self.imageDect = ActionPicturesDetectionThread()
        self.imageDect.infoEmit.connect(self._infoEmitEvent)
        self.imageDect.overEmit.connect(self.killRealTimeDetectionThread)
        self.videoDect = ActionVideoDetectionThread()
        self.videoDect.infoEmit.connect(self._infoEmitEvent)
        self.videoDect.overEmit.connect(self.killRealTimeDetectionThread)
        self.videoDect.stopVideoDetectionEmit.connect(self.videoDect.setViolenceStop)
        self.button_imagePath.clicked.connect(self.imageDetection)
        self.button_imagePath_2.clicked.connect(self.imagesDetection)

        self.label_image.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.label_image.customContextMenuRequested.connect(self.labelEvent)  # 开放右键策略

        # 默认选中按钮
        self.checkBox_person.setChecked(True)
        self.checkBox_bicycle.setChecked(True)
        self.checkBox_bus.setChecked(True)
        self.checkBox_car.setChecked(True)
        self.checkBox_truck.setChecked(True)
        self.checkBox_train.setChecked(True)
        self.radioButton_selectAll.setChecked(True)
        self.radioButton_selectAll.clicked.connect(self.setSelectAll)
        self.radioButton_noSelect.clicked.connect(self.noSelect)

        self.checkBox_saveAVI.setChecked(True)

        self.radioButton_showImages.setChecked(True)
        self.dial.valueChanged.connect(self.dialSetSpeedThre)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_5.setTitle(_translate("Form", "识别目标"))
        self.checkBox_person.setText(_translate("Form", "行人"))
        self.checkBox_bicycle.setText(_translate("Form", "自行车"))
        self.checkBox_car.setText(_translate("Form", "汽车"))
        self.checkBox_truck.setText(_translate("Form", "卡车"))
        self.checkBox_bus.setText(_translate("Form", "公交车"))
        self.checkBox_train.setText(_translate("Form", "火车"))
        self.radioButton_selectAll.setText(_translate("Form", "全选（默认）"))
        self.radioButton_noSelect.setText(_translate("Form", "全不选"))
        self.checkBox_saveFrame.setText(_translate("Form", "保存视频识别帧(工作空间）"))
        self.checkBox_saveAVI.setText(_translate("Form", "保存识别后视频"))
        self.checkBox_onlyDect.setText(_translate("Form", "仅检测不跟踪模式"))
        self.button_start.setText(_translate("Form", "开始"))
        self.button_over.setText(_translate("Form", "强制终止"))
        self.label_3.setText(_translate("Form", "拨轮限速："))
        self.label_7.setText(_translate("Form", "限速:"))
        self.label_8.setText(_translate("Form", "距离："))
        self.label_5.setText(_translate("Form", "FPS："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), _translate("Form", "视频识别"))
        self.checkBox_autoSaveImage.setText(_translate("Form", "自动保存结果到工作空间"))
        self.label_2.setText(_translate("Form", "识别模式："))
        self.comboBox_mode.setItemText(0, _translate("Form", "目标检测与数量统计"))
        self.comboBox_mode.setItemText(1, _translate("Form", "道路归属与车牌识别"))
        self.radioButton_tipShowImages.setText(_translate("Form", "多张影像弹出窗展示"))
        self.radioButton_showImages.setText(_translate("Form", "多张影像逐张显示"))
        self.groupBox_3.setTitle(_translate("Form", "单张影像识别"))
        self.label.setText(_translate("Form", "图像路径"))
        self.groupBox_4.setTitle(_translate("Form", "多张影像批量识别"))
        self.label_6.setText(_translate("Form", "图像列"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage3), _translate("Form", "图像识别"))
        self.groupBox_2.setTitle(_translate("Form", "实时监测信息"))

    def setSelectAll(self):
        self.checkBox_person.setChecked(True)
        self.checkBox_bicycle.setChecked(True)
        self.checkBox_bus.setChecked(True)
        self.checkBox_car.setChecked(True)
        self.checkBox_truck.setChecked(True)
        self.checkBox_train.setChecked(True)

    def noSelect(self):
        self.checkBox_person.setChecked(False)
        self.checkBox_bicycle.setChecked(False)
        self.checkBox_bus.setChecked(False)
        self.checkBox_car.setChecked(False)
        self.checkBox_truck.setChecked(False)
        self.checkBox_train.setChecked(False)

    def getDetectionTarget(self):
        """
        兴趣值参数
        :return: Dictionary Type & None
        """
        COI = []
        if self.checkBox_person.isChecked():
            COI.append("person")
        if self.checkBox_bicycle.isChecked():
            COI.append("bicycle")
        if self.checkBox_bus.isChecked():
            COI.append("bus")
        if self.checkBox_car.isChecked():
            COI.append("car")
        if self.checkBox_truck.isChecked():
            COI.append("truck")
        if self.checkBox_train.isChecked():
            COI.append("train")

        if len(COI) != 0:
            return COI
        else:
            return None

    def dectVideo(self):
        path = Database.videoPath
        if isinstance(path, str):
            # 获取参数
            saveAVI = False
            onlyDetectionMode = False
            if self.checkBox_saveAVI.isChecked():
                saveAVI = True
            if self.checkBox_onlyDect.isChecked():
                onlyDetectionMode = True
            if self.checkBox_saveFrame.isChecked():  # 从显示的地方调换，只执行一次，节省空间
                # 创建目录
                (dir, videoName) = os.path.split(path)
                videoName = videoName.split(".")[0]
                self.frameDir = Database.workspace + "/" + videoName + "_FRAME_RESULT"
                if os.path.exists(self.frameDir) is False:  # 路径不存在，创建
                    os.mkdir(self.frameDir)

            dictPara = {
                "type": "200",
                "path": path,
                "camParamPath": Database.camParamPath,
                "COI": self.getDetectionTarget(),
                "avi": saveAVI,
                "onlyDect": onlyDetectionMode,
                "dis_thre": self.spinBox_distance.value(),
                "speed_thre": self.spinBox_speed.value()
            }
            self.startVideoDectThread(dictPara)
            # 设定视频检测状态
            Database.videoDetecting = True
        else:
            self._infoEmitEvent("V", "请先导入需要检测的视频！")
            self._infoEmitEvent("W", "请先导入需要检测的视频！")

    def imageDetection(self):
        filePath, type = QtWidgets.QFileDialog.getOpenFileName(self.parent(), "导入图像", Database.workspace,
                                                               "JPEG(*JPG);;PNG(*PNG);;TIFF(*.TIF);;All Files (*)")
        if filePath != "":
            (dir, videoName) = os.path.split(filePath)
            self._infoEmitEvent("file", dir)
            dictPara = {
                "type": "201",
                "path": filePath,
                "COI": self.getDetectionTarget(),
                "autoSave": self.checkBox_autoSaveImage.isChecked(),  # True/False
                "mode": self.comboBox_mode.currentIndex()  # 0/1
            }
            self.startImagesDectThread(dictPara)
        else:
            self._infoEmitEvent("T", "提示：已取消导入图像")

    def imagesDetection(self):
        filePaths, type = QtWidgets.QFileDialog.getOpenFileNames(self.parent(), "批量导入图像", Database.workspace,
                                                                 "JPEG(*JPG);;PNG(*PNG);;TIFF(*.TIF);;BMP(*.bmp);;All Files (*)")

        if len(filePaths) > 0:
            # 显示路径到界面
            (dir, videoName) = os.path.split(filePaths[0])
            self._infoEmitEvent("file", dir)
            # 获取展示方式
            showWait = True
            if self.radioButton_showImages.isChecked():
                showWait = True
            elif self.radioButton_tipShowImages.isChecked():
                showWait = False

            dictPara = {
                "type": "202",
                "path": filePaths,
                "COI": self.getDetectionTarget(),
                "show": showWait,
                "autoSave": self.checkBox_autoSaveImage.isChecked(),  # True/False
                "mode": self.comboBox_mode.currentIndex()  # 0/1
            }
            # 启动线程
            self.startImagesDectThread(dictPara)
        else:
            pass
            # self._infoEmitEvent("T", "已取消批量导入图像")

    def startVideoDectThread(self, dictPara):
        self.videoDect.setPara(dictPara)
        self._infoEmitEvent("I", "开启视频识别线程！")
        self.videoDect.start()
        self._infoEmitEvent("I", "线程已经开启,加载模型中.......")

    def startImagesDectThread(self, dictPara):
        self.imageDect.setPara(dictPara)
        self._infoEmitEvent("I", "开启线程！")
        self.imageDect.start()
        self._infoEmitEvent("I", "线程已经开启,加载模型中.......")

    def killRealTimeDetectionThread(self):
        self.imageDect.killThread()
        self.videoDect.killThread()
        self._infoEmitEvent("I", " - 子线程关闭.\n")

    def _infoEmitEvent(self, type, infoStr):
        """
        顶层信号槽函数
        :param type: I-信息
        :param infoStr:
        :return:
        """
        if type == "M":
            self.setVideoFrame()
        elif type == "F":
            self.setFPS(infoStr)
            # 同时启动一个保存

        elif type == "file":
            self.infoEmit.emit("F", infoStr)
        elif type == "A":
            result = Database.imageResult
            self._setLabelPixmap(result["image"])
            self._infoEmitEvent("I", str(result["COI"]))  # 自迭代回调显示COI信息
        elif type == "videoDetecting":  # 视频检测状态
            Database.videoDetecting = False
        else:
            self.infoEmit.emit(type, infoStr)

    def setFPS(self, strValue):
        self.count += 1
        if self.count >= 89:
            self.count = 0
        self.lcdNumber.setProperty("value", float(strValue))

    def dialSetSpeedThre(self):
        self.spinBox_speed.setValue(self.dial.value())

    def violenceStop(self):
        """
        暴力终止视频识别进程
        :return:
        """
        if Database.videoDetecting:
            self._infoEmitEvent("V", "警告！当前操作将强制终止视频检测进程！是否继续执行该操作")
            user_action = ActionWarnException(self.parent()).actionWarnException("R", "警告！当前操作将强制终止视频检测进程！\n是否继续执行该操作")
            if user_action:
                self._infoEmitEvent("I", "\n发送终止信号...")
                self.videoDect.stopVideoDetectionEmit.emit()
                # TODO 待优化问题
                # self.killRealTimeDetectionThread()
                self._infoEmitEvent("I", "已强制终止进程!")
                Database.videoDetecting = False  # 恢复视频检测状态
            else:
                self._infoEmitEvent("I", "已取消强制终止操作,继续检测中...")
        else:
            self._infoEmitEvent("I", "当前无视频在进行检测")

    def setVideoFrame(self):
        """
        设置视频识别的结果
        :return:
        """
        try:
            # 从队列缓冲区获取图像信息
            self.queueIm = Queue()
            RGBImage = self.queueIm.getImageStrak()
            RGBImage = RGBImage.toqpixmap()
            # self.report()

            if self.tabWidget.currentIndex() == 0 and self.checkBox_saveFrame.isChecked():  # 视频识别保存帧功能
                RGBImage.save(self.frameDir + "/" + str(self.frameCount) + ".jpg")
                self.frameCount += 1  # 不加上这个的话,一个图像名就会不断刷新保存，变成假视频

            if RGBImage != None:
                # print("相框大小", self.label_image.width(), self.label_image.height())
                # 通过测试，相框self.label_image.height()在设定每一帧图像后都会+1，故每次设定-1
                # 由于之前已经设定过帧图像，无法继续因为-1而缩小（这也是设定图像后无法最小化到正常状态的原因之一），故而实现界面固定
                jpg_out = QtGui.QPixmap(RGBImage).scaled(self.label_image.width(),
                                                         self.label_image.height() - 1)  # 设置图片大小
                self.label_image.setPixmap(QtGui.QPixmap(jpg_out))
        except Exception as e:
            self._infoEmitEvent("E", "异常警告：" + e.__str__())

    def _setLabelPixmap(self, image):
        """
        图像显示到界面
        :param image: Image类型图像
        :return:
        """
        image = image.toqpixmap()
        self.label_image.setPixmap(
            QtGui.QPixmap(QtGui.QPixmap(image).scaled(self.label_image.width(), self.label_image.height())))

    def labelEvent(self):
        """
        label区域右键菜单功能
        :return:
        """
        picture = fromqpixmap(self.label_image.pixmap())
        filePath, k = QtWidgets.QFileDialog.getSaveFileName(self.parent(), "保存图像", Database.workspace,
                                                            "JPEG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        if filePath != "":
            picture.save(filePath)
        else:
            self._infoEmitEvent("I", "取消手动保存识别后影像")
