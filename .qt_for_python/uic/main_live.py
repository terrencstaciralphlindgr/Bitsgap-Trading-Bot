# Form implementation generated from reading ui file 'e:\Task\Richard\main_live.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(False)
        MainWindow.resize(861, 726)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(861, 726))
        MainWindow.setMaximumSize(QtCore.QSize(861, 726))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 291, 691))
        self.groupBox.setObjectName("groupBox")
        self.mt_table = QtWidgets.QTableWidget(self.groupBox)
        self.mt_table.setGeometry(QtCore.QRect(10, 20, 271, 531))
        self.mt_table.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop)
        self.mt_table.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.mt_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.mt_table.setShowGrid(True)
        self.mt_table.setWordWrap(False)
        self.mt_table.setRowCount(100)
        self.mt_table.setColumnCount(2)
        self.mt_table.setObjectName("mt_table")
        item = QtWidgets.QTableWidgetItem()
        self.mt_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.mt_table.setHorizontalHeaderItem(1, item)
        self.mt_table.horizontalHeader().setVisible(True)
        self.mt_table.horizontalHeader().setCascadingSectionResizes(False)
        self.mt_table.horizontalHeader().setDefaultSectionSize(110)
        self.mt_table.horizontalHeader().setHighlightSections(True)
        self.mt_table.verticalHeader().setDefaultSectionSize(25)
        self.mt_table.verticalHeader().setMinimumSectionSize(25)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(80, 610, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.mt_collective = QtWidgets.QLabel(self.groupBox)
        self.mt_collective.setGeometry(QtCore.QRect(180, 610, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mt_collective.setFont(font)
        self.mt_collective.setObjectName("mt_collective")
        self.mt_viewchart = QtWidgets.QPushButton(self.groupBox)
        self.mt_viewchart.setGeometry(QtCore.QRect(10, 640, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mt_viewchart.setFont(font)
        self.mt_viewchart.setObjectName("mt_viewchart")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 560, 131, 41))
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.mt_profit = QtWidgets.QLineEdit(self.groupBox_3)
        self.mt_profit.setGeometry(QtCore.QRect(0, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.mt_profit.setFont(font)
        self.mt_profit.setPlaceholderText("")
        self.mt_profit.setObjectName("mt_profit")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(150, 560, 131, 41))
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.mt_stoploss = QtWidgets.QLineEdit(self.groupBox_4)
        self.mt_stoploss.setGeometry(QtCore.QRect(0, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(False)
        self.mt_stoploss.setFont(font)
        self.mt_stoploss.setPlaceholderText("")
        self.mt_stoploss.setObjectName("mt_stoploss")
        self.mt_clearchart = QtWidgets.QPushButton(self.groupBox)
        self.mt_clearchart.setGeometry(QtCore.QRect(150, 640, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mt_clearchart.setFont(font)
        self.mt_clearchart.setObjectName("mt_clearchart")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(320, 10, 531, 691))
        self.groupBox_2.setObjectName("groupBox_2")
        self.st_table = QtWidgets.QTableWidget(self.groupBox_2)
        self.st_table.setGeometry(QtCore.QRect(10, 20, 511, 661))
        self.st_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.st_table.setWordWrap(False)
        self.st_table.setRowCount(100)
        self.st_table.setColumnCount(6)
        self.st_table.setObjectName("st_table")
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.st_table.setHorizontalHeaderItem(5, item)
        self.st_table.horizontalHeader().setDefaultSectionSize(76)
        self.st_table.verticalHeader().setDefaultSectionSize(25)
        self.st_table.verticalHeader().setMinimumSectionSize(25)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bitsgap Bot Manager - Live"))
        self.groupBox.setTitle(_translate("MainWindow", "MULTIPLE TRADES"))
        item = self.mt_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Pair"))
        item = self.mt_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Change %"))
        self.label.setText(_translate("MainWindow", "Collective %:"))
        self.mt_collective.setText(_translate("MainWindow", "0"))
        self.mt_viewchart.setText(_translate("MainWindow", "View Chart"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Take Profit"))
        self.mt_profit.setText(_translate("MainWindow", "2"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Stop Loss"))
        self.mt_stoploss.setText(_translate("MainWindow", "-2"))
        self.mt_clearchart.setText(_translate("MainWindow", "Clear Chart"))
        self.groupBox_2.setTitle(_translate("MainWindow", "SINGLE TRADES"))
        item = self.st_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Pair"))
        item = self.st_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Change %"))
        item = self.st_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Take Profit"))
        item = self.st_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Stop Loss"))
        item = self.st_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Chart"))
        item = self.st_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Clear"))
