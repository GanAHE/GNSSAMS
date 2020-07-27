#!usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# 作者：神秘藏宝室
# 添加
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MyBrowser(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        htmlfile = "gpsPoint.html"
        url = QUrl(htmlfile)
        self.webView.load(url)
        self.webView.loadFinished.connect(self._plot)

        print
        u"html载入"
        # self.createConnection()

    # def createConnection(self):
    #     # self.connect(self.pushButtonGo,SIGNAL("clicked"),self.on_pushButtonGo_clicked)
    #     self.pushButtonGo.clicked.connect(self.on_pushButtonGo_clicked)

    @pyqtSlot(result="QString")
    def _plot(self):
        self.webView.page().mainFrame().evaluateJavaScript('theNewLocation(112.424483,34.640631);')

    @pyqtSignature("")
    def on_lineEditAddress_returnPressed(self):
        """
        Slot documentation goes here.
        """
        self.search()

    @pyqtSignature("")
    def on_pushButtonGo_clicked(self):
        """
        Slot documentation goes here.
        """
        self.search()

    def search(self):
        address = str(self.lineEditAddress.text())
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
                self.lineEditAddress.setText(address)
            url = QUrl(address)
            self.webView.load(url)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mb = MyBrowser()
    mb.show()
    sys.exit(app.exec_())