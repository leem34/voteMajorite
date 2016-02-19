# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VM_pol.ui'
#
# Created: Wed Feb 10 13:04:35 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(340, 56)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_pol_1 = QtGui.QLabel(Form)
        self.label_pol_1.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_pol_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_pol_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_pol_1.setLineWidth(2)
        self.label_pol_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pol_1.setObjectName(_fromUtf8("label_pol_1"))
        self.gridLayout.addWidget(self.label_pol_1, 0, 0, 1, 1)
        self.label_pol_2 = QtGui.QLabel(Form)
        self.label_pol_2.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_pol_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_pol_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_pol_2.setLineWidth(2)
        self.label_pol_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pol_2.setObjectName(_fromUtf8("label_pol_2"))
        self.gridLayout.addWidget(self.label_pol_2, 0, 1, 1, 1)
        self.label_pol_3 = QtGui.QLabel(Form)
        self.label_pol_3.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_pol_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_pol_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_pol_3.setLineWidth(2)
        self.label_pol_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pol_3.setObjectName(_fromUtf8("label_pol_3"))
        self.gridLayout.addWidget(self.label_pol_3, 0, 2, 1, 1)
        self.label_pol_4 = QtGui.QLabel(Form)
        self.label_pol_4.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_pol_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_pol_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_pol_4.setLineWidth(2)
        self.label_pol_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pol_4.setObjectName(_fromUtf8("label_pol_4"))
        self.gridLayout.addWidget(self.label_pol_4, 0, 3, 1, 1)
        self.label_val_1 = QtGui.QLabel(Form)
        self.label_val_1.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_val_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_val_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_val_1.setLineWidth(2)
        self.label_val_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_1.setObjectName(_fromUtf8("label_val_1"))
        self.gridLayout.addWidget(self.label_val_1, 1, 0, 1, 1)
        self.label_val_2 = QtGui.QLabel(Form)
        self.label_val_2.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_val_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_val_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_val_2.setLineWidth(2)
        self.label_val_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_2.setObjectName(_fromUtf8("label_val_2"))
        self.gridLayout.addWidget(self.label_val_2, 1, 1, 1, 1)
        self.label_val_3 = QtGui.QLabel(Form)
        self.label_val_3.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_val_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_val_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_val_3.setLineWidth(2)
        self.label_val_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_3.setObjectName(_fromUtf8("label_val_3"))
        self.gridLayout.addWidget(self.label_val_3, 1, 2, 1, 1)
        self.label_val_4 = QtGui.QLabel(Form)
        self.label_val_4.setStyleSheet(_fromUtf8("border: 2px solid black;\n"
"font-weight: bold;"))
        self.label_val_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label_val_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_val_4.setLineWidth(2)
        self.label_val_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_4.setObjectName(_fromUtf8("label_val_4"))
        self.gridLayout.addWidget(self.label_val_4, 1, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_pol_1.setText(_translate("Form", "TextLabel", None))
        self.label_pol_2.setText(_translate("Form", "TextLabel", None))
        self.label_pol_3.setText(_translate("Form", "TextLabel", None))
        self.label_pol_4.setText(_translate("Form", "TextLabel", None))
        self.label_val_1.setText(_translate("Form", "TextLabel", None))
        self.label_val_2.setText(_translate("Form", "TextLabel", None))
        self.label_val_3.setText(_translate("Form", "TextLabel", None))
        self.label_val_4.setText(_translate("Form", "TextLabel", None))

