# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imagesDetectionWight.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import io
import os

import PIL
from PIL.Image import fromqpixmap
from PyQt5 import QtCore, QtGui, QtWidgets

from database.database import Database
import matplotlib.pyplot as plt

from database.imageQueue import Queue
from window.actionOperate.actionPicturesDetectionThread import ActionPicturesDetectionThread


class Ui_Form(QtCore.QObject):
    infoEmit = QtCore.pyqtSignal(str, str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1219, 704)

        # 为了弹出窗的美观
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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
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
        self.groupBox_6.setStyleSheet("")
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
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_autoSaveImage = QtWidgets.QCheckBox(self.groupBox_7)
        self.checkBox_autoSaveImage.setObjectName("checkBox_autoSaveImage")
        self.verticalLayout.addWidget(self.checkBox_autoSaveImage)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_2 = QtWidgets.QLabel(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_11.addWidget(self.label_2)
        self.comboBox_mode = QtWidgets.QComboBox(self.groupBox_7)
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.horizontalLayout_11.addWidget(self.comboBox_mode)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.radioButton_tipShowImages = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton_tipShowImages.setObjectName("radioButton_tipShowImages")
        self.verticalLayout.addWidget(self.radioButton_tipShowImages)
        self.radioButton_showImages = QtWidgets.QRadioButton(self.groupBox_7)
        self.radioButton_showImages.setObjectName("radioButton_showImages")
        self.verticalLayout.addWidget(self.radioButton_showImages)
        self.verticalLayout_2.addWidget(self.groupBox_7)
        self.line_5 = QtWidgets.QFrame(self.groupBox)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_2.addWidget(self.line_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setStyleSheet("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.button_imagePath = QtWidgets.QPushButton(self.groupBox_3)
        self.button_imagePath.setStyleSheet("background-color: rgb(215, 255, 249);")
        self.button_imagePath.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./source/icon/more.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_imagePath.setIcon(icon)
        self.button_imagePath.setCheckable(False)
        self.button_imagePath.setAutoRepeat(False)
        self.button_imagePath.setAutoExclusive(False)
        self.button_imagePath.setObjectName("button_imagePath")
        self.horizontalLayout_6.addWidget(self.button_imagePath)
        self.horizontalLayout_9.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.button_imagePath_2 = QtWidgets.QPushButton(self.groupBox_4)
        self.button_imagePath_2.setStyleSheet("background-color: rgb(215, 255, 249);")
        self.button_imagePath_2.setText("")
        self.button_imagePath_2.setIcon(icon)
        self.button_imagePath_2.setObjectName("button_imagePath_2")
        self.horizontalLayout_8.addWidget(self.button_imagePath_2)
        self.horizontalLayout_9.addWidget(self.groupBox_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.label_fig = QtWidgets.QLabel(self.groupBox)
        self.label_fig.setStyleSheet("background-color: rgb(242, 251, 255);")
        self.label_fig.setText("")
        self.label_fig.setPixmap(QtGui.QPixmap("./source/icon/icon_any.png"))
        self.label_fig.setScaledContents(False)
        self.label_fig.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fig.setObjectName("label_fig")
        self.verticalLayout_2.addWidget(self.label_fig)
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

        self.imageDect = ActionPicturesDetectionThread()
        self.imageDect.infoEmit.connect(self._infoEmitEvent)
        self.imageDect.overEmit.connect(self.killRealTimeDetectionThread)
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

        self.radioButton_showImages.setChecked(True)

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
            self._infoEmitEvent("I", "提示：已取消导入图像")

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
            self._infoEmitEvent("I", "已取消批量导入图像")

    def startImagesDectThread(self, dictPara):
        self.imageDect.setPara(dictPara)
        self._infoEmitEvent("I", "开启线程！")
        self.imageDect.start()
        self._infoEmitEvent("I", "线程已经开启,加载模型中.......")

    def killRealTimeDetectionThread(self):
        self.imageDect.killThread()
        self._infoEmitEvent("I", " - 子线程关闭.\n")

    def _infoEmitEvent(self, type, infoStr):
        """
        顶层信号槽函数
        :param type: I-信息
        :param infoStr:
        :return:
        """
        if type == "M":
            self.setDetectedPicture()
        elif type == "file":
            self.infoEmit.emit("F", infoStr)
        elif type == "A":
            # 图像目标识别
            result = Database.imageResult
            self._setLabelPixmap(result["image"])
            # 设定小窗口显示
            if self.comboBox_mode.currentIndex() == 0:
                self.setLabelFig(result["COI"])
            else:
                # 恢复默认
                self.label_fig.setPixmap(QtGui.QPixmap("./source/icon/icon_any.png"))

            self._infoEmitEvent("I", str(result["COI"]))  # 自迭代回调显示COI信息
        elif type == "videoDetecting":  # 视频检测状态
            Database.videoDetecting = False
        else:
            self.infoEmit.emit(type, infoStr)

    def setDetectedPicture(self):
        """
        设置多张图像的结果
        :return: None
        """
        try:
            # 从队列缓冲区获取图像信息
            self.queueIm = Queue()
            RGBImage = self.queueIm.getImageStrak()
            RGBImage = RGBImage.toqpixmap()
            if RGBImage != None:
                jpg_out = QtGui.QPixmap(RGBImage).scaled(self.label_image.width(), self.label_image.height())  # 设置图片大小
                self.label_image.setPixmap(QtGui.QPixmap(jpg_out))

                # 设定小窗口显示可视化结果
                if self.comboBox_mode.currentIndex() == 0:
                    COI = self.queueIm.getImageCOI()
                    print(type(COI), COI)
                    self.setLabelFig(COI)
                else:
                    # 恢复默认
                    self.label_fig.setPixmap(QtGui.QPixmap("./source/icon/icon_any.png"))

        except Exception as e:
            self._infoEmitEvent("E", "异常警告：" + e.__str__())

    def _setLabelPixmap(self, image, lacation=None):
        """
        图像显示到界面
        :param image: Image类型图像
        :return:
        """
        image = image.toqpixmap()
        if lacation is None:
            self.label_image.setPixmap(
                QtGui.QPixmap(QtGui.QPixmap(image).scaled(self.label_image.width(), self.label_image.height())))
        else:
            self.label_fig.setPixmap(
                QtGui.QPixmap(QtGui.QPixmap(image).scaled(self.label_fig.width(), self.label_fig.height())))

    def setLabelFig(self, DetectDict, showDialog=False):
        """
        单张图像绘制检测数目
        :param DetectDict:
        :param fig:
        :return:
        """
        try:
            judge = list(DetectDict.values())[0]
            if judge is not None:
                # 默认直方图
                fig = self.drawCOIResult(DetectDict, "bar")
                # 展示方式
                if showDialog:
                    fig.show()
                else:
                    buffer_ = io.BytesIO()
                    fig.savefig(buffer_, format="png")
                    buffer_.seek(0)
                    self._setLabelPixmap(PIL.Image.open(buffer_), lacation="fig")
                    buffer_.close()
        except Exception as e:
            self._infoEmitEvent("E", "统计数据可视化出现异常：" + e.__str__())

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

    def drawCOIResult(self, COIDict, type):
        """
        将COI返回的结果字典值绘制成条形图或饼状图
        :param COIDict:
        :param type:
        :return:
        """
        name = list(COIDict.keys())
        value = list(COIDict.values())
        if type == "bar":
            plt.bar(name, value, edgecolor='green', label="The count of detector", lw=3)
            # 添加数据标签，也就是给柱子顶部添加标签
            for a, b in zip(name, value):
                plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
            plt.legend(loc='upper left')
            return plt
        elif type == "pie":
            plt.pie(value, labels=name, shadow=True, startangle=60)
            plt.title("detect Count")
            plt.legend(loc='upper left')
            plt.axis('equal')
            return plt
