# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.showOnlineButton = QtWidgets.QPushButton(Dialog)
        self.showOnlineButton.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.showOnlineButton.setObjectName("showOnlineButton")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 151, 211))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setGeometry(QtCore.QRect(170, 70, 151, 211))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 50, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(180, 50, 47, 13))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.showOnlineButton.setText(_translate("Dialog", "Показать"))
        self.label.setText(_translate("Dialog", "IDs"))
        self.label_2.setText(_translate("Dialog", "Dates"))
