# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
import sys
from octree_4_3 import *

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_input = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_input.setGeometry(QtCore.QRect(540, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.pushButton_input.setFont(font)
        self.pushButton_input.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_input.setObjectName("pushButton_input")
        self.lineEdit_input = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_input.setGeometry(QtCore.QRect(40, 40, 451, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.lineEdit_input.setFont(font)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.lineEdit_output = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_output.setGeometry(QtCore.QRect(40, 110, 451, 31))
        self.lineEdit_output.setAcceptDrops(True)
        self.lineEdit_output.setFrame(True)
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.pushButton_output = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_output.setGeometry(QtCore.QRect(540, 110, 181, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.pushButton_output.setFont(font)
        self.pushButton_output.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_output.setObjectName("pushButton_output")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 170, 801, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 220, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 280, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinBox_minChildBoxes = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_minChildBoxes.setGeometry(QtCore.QRect(240, 340, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.spinBox_minChildBoxes.setFont(font)
        self.spinBox_minChildBoxes.setProperty("value", 8)
        self.spinBox_minChildBoxes.setObjectName("spinBox_minChildBoxes")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 340, 121, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.spinBox_maxLevel = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_maxLevel.setGeometry(QtCore.QRect(240, 220, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.spinBox_maxLevel.setFont(font)
        self.spinBox_maxLevel.setMinimum(1)
        self.spinBox_maxLevel.setProperty("value", 6)
        self.spinBox_maxLevel.setObjectName("spinBox_maxLevel")
        self.spinBox_minLevel = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_minLevel.setGeometry(QtCore.QRect(240, 280, 61, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.spinBox_minLevel.setFont(font)
        self.spinBox_minLevel.setMinimum(1)
        self.spinBox_minLevel.setProperty("value", 4)
        self.spinBox_minLevel.setObjectName("spinBox_minLevel")
        self.checkBox_cubic = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_cubic.setGeometry(QtCore.QRect(100, 410, 71, 20))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.checkBox_cubic.setFont(font)
        self.checkBox_cubic.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_cubic.setChecked(True)
        self.checkBox_cubic.setObjectName("checkBox_cubic")
        self.checkBox_backTrack = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_backTrack.setGeometry(QtCore.QRect(200, 410, 101, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.checkBox_backTrack.setFont(font)
        self.checkBox_backTrack.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_backTrack.setChecked(True)
        self.checkBox_backTrack.setObjectName("checkBox_backTrack")
        self.textEdit_info = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_info.setGeometry(QtCore.QRect(420, 210, 341, 321))
        self.textEdit_info.setObjectName("textEdit_info")
        self.pushButton_apply = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_apply.setGeometry(QtCore.QRect(130, 470, 131, 51))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.pushButton_apply.setFont(font)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.label_stat = QtWidgets.QLabel(self.centralwidget)
        self.label_stat.setGeometry(QtCore.QRect(0, 570, 781, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_stat.setFont(font)
        self.label_stat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_stat.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stat.setObjectName("label_stat")
        self.pushButton_input.raise_()
        self.pushButton_output.raise_()
        self.lineEdit_input.raise_()
        self.lineEdit_output.raise_()
        self.line.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.spinBox_minChildBoxes.raise_()
        self.label_3.raise_()
        self.spinBox_maxLevel.raise_()
        self.spinBox_minLevel.raise_()
        self.checkBox_cubic.raise_()
        self.checkBox_backTrack.raise_()
        self.textEdit_info.raise_()
        self.pushButton_apply.raise_()
        self.label_stat.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        self.pushButton_input.clicked.connect(self.chooseSTL)
        self.pushButton_output.clicked.connect(self.chooseOutput)
        self.pushButton_apply.clicked.connect(self.run)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voxelization"))
        self.pushButton_input.setText(_translate("MainWindow", "Choose STL file"))
        self.pushButton_output.setText(_translate("MainWindow", "Choose output path "))
        self.label.setText(_translate("MainWindow", "maxLevel"))
        self.label_2.setText(_translate("MainWindow", "minLevel"))
        self.label_3.setText(_translate("MainWindow", "minChildBoxes"))
        self.checkBox_cubic.setText(_translate("MainWindow", "cubic"))
        self.checkBox_backTrack.setText(_translate("MainWindow", "backTrack"))
        self.pushButton_apply.setText(_translate("MainWindow", "Voxelization"))
        self.label_stat.setText(_translate("MainWindow", "Octree voxelization application made by zzw"))

    def chooseSTL(self):
        stlFile,type = QFileDialog.getOpenFileName(self.MainWindow,"Choose STL file",os.getcwd(),"STL files(*.stl);;Txt files(*.txt)")
        self.lineEdit_input.setText(stlFile)

    def chooseOutput(self):
        outputPath,type = QFileDialog.getSaveFileName(self.MainWindow,"Choose output path",os.getcwd(),"Txt files(*.txt)")
        self.lineEdit_output.setText(outputPath)

    def run(self):
        self.label_stat.setText("Running")
        print("Running")
        stlFile = self.lineEdit_input.text()
        output = self.lineEdit_output.text()
        maxLevel = self.spinBox_maxLevel.value()
        minLevel = self.spinBox_minLevel.value()
        minChildBoxes = self.spinBox_minChildBoxes.value()
        cubic = True if self.checkBox_cubic.checkState()==QtCore.Qt.Checked else False

        tree = Octree(stlFile, maxLevel, minLevel, minChildBoxes, cubic)
        tree.traverse()
        if self.checkBox_backTrack.checkState()==QtCore.Qt.Checked:
            print("------Trackback------")
            tree.backtrack()
        tree.writeBoxes(output)
        self.label_stat.setText("Finished! All {} triangles!".format(len(tree.triangles)))

    def normalOutputWritten(self,text):
        cursor = self.textEdit_info.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_info.setTextCursor(cursor)
        self.textEdit_info.ensureCursorVisible()


    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

