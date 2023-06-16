# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Vaccine_Add_Edit.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_winVaccineAddEdit(object):
    def setupUi(self, winVaccineAddEdit):
        winVaccineAddEdit.setObjectName("winVaccineAddEdit")
        winVaccineAddEdit.resize(480, 180)
        icon = QtGui.QIcon.fromTheme("C:\\Users\\baris\\Desktop\\Projects\\Vet\\Icons\\Cosmos_Vet.ico")
        winVaccineAddEdit.setWindowIcon(icon)
        self.lblDateOfAppointment = QtWidgets.QLabel(winVaccineAddEdit)
        self.lblDateOfAppointment.setGeometry(QtCore.QRect(38, 50, 145, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.lblDateOfAppointment.setFont(font)
        self.lblDateOfAppointment.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblDateOfAppointment.setStyleSheet("")
        self.lblDateOfAppointment.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDateOfAppointment.setObjectName("lblDateOfAppointment")
        self.dtDateOfAppointment = QtWidgets.QDateEdit(winVaccineAddEdit)
        self.dtDateOfAppointment.setEnabled(True)
        self.dtDateOfAppointment.setGeometry(QtCore.QRect(190, 50, 250, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.dtDateOfAppointment.setFont(font)
        self.dtDateOfAppointment.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dtDateOfAppointment.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dtDateOfAppointment.setAutoFillBackground(False)
        self.dtDateOfAppointment.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(74, 74, 74);")
        self.dtDateOfAppointment.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.dtDateOfAppointment.setAlignment(QtCore.Qt.AlignCenter)
        self.dtDateOfAppointment.setReadOnly(False)
        self.dtDateOfAppointment.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dtDateOfAppointment.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.dtDateOfAppointment.setCalendarPopup(True)
        self.dtDateOfAppointment.setTimeSpec(QtCore.Qt.LocalTime)
        self.dtDateOfAppointment.setObjectName("dtDateOfAppointment")
        self.dtDateOfVaccination = QtWidgets.QDateEdit(winVaccineAddEdit)
        self.dtDateOfVaccination.setEnabled(True)
        self.dtDateOfVaccination.setGeometry(QtCore.QRect(190, 80, 250, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.dtDateOfVaccination.setFont(font)
        self.dtDateOfVaccination.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dtDateOfVaccination.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dtDateOfVaccination.setAutoFillBackground(False)
        self.dtDateOfVaccination.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(74, 74, 74);")
        self.dtDateOfVaccination.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.dtDateOfVaccination.setAlignment(QtCore.Qt.AlignCenter)
        self.dtDateOfVaccination.setReadOnly(False)
        self.dtDateOfVaccination.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dtDateOfVaccination.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.dtDateOfVaccination.setCalendarPopup(True)
        self.dtDateOfVaccination.setTimeSpec(QtCore.Qt.LocalTime)
        self.dtDateOfVaccination.setObjectName("dtDateOfVaccination")
        self.lblDateOfVaccination = QtWidgets.QLabel(winVaccineAddEdit)
        self.lblDateOfVaccination.setGeometry(QtCore.QRect(38, 80, 145, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.lblDateOfVaccination.setFont(font)
        self.lblDateOfVaccination.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblDateOfVaccination.setStyleSheet("")
        self.lblDateOfVaccination.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDateOfVaccination.setObjectName("lblDateOfVaccination")
        self.entNameofVaccine = QtWidgets.QLineEdit(winVaccineAddEdit)
        self.entNameofVaccine.setGeometry(QtCore.QRect(190, 24, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.entNameofVaccine.setFont(font)
        self.entNameofVaccine.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.entNameofVaccine.setObjectName("entNameofVaccine")
        self.lblNameofVaccine = QtWidgets.QLabel(winVaccineAddEdit)
        self.lblNameofVaccine.setGeometry(QtCore.QRect(38, 24, 145, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.lblNameofVaccine.setFont(font)
        self.lblNameofVaccine.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblNameofVaccine.setStyleSheet("")
        self.lblNameofVaccine.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblNameofVaccine.setObjectName("lblNameofVaccine")
        self.btnSave = QtWidgets.QPushButton(winVaccineAddEdit)
        self.btnSave.setGeometry(QtCore.QRect(215, 120, 50, 50))
        self.btnSave.setStatusTip("")
        self.btnSave.setText("")
        icon = QtGui.QIcon.fromTheme("C:\\Users\\baris\\Desktop\\Projects\\Vet\\Icons\\save.png")
        self.btnSave.setIcon(icon)
        self.btnSave.setIconSize(QtCore.QSize(40, 40))
        self.btnSave.setFlat(True)
        self.btnSave.setObjectName("btnSave")

        self.retranslateUi(winVaccineAddEdit)
        QtCore.QMetaObject.connectSlotsByName(winVaccineAddEdit)
        winVaccineAddEdit.setTabOrder(self.entNameofVaccine, self.dtDateOfAppointment)
        winVaccineAddEdit.setTabOrder(self.dtDateOfAppointment, self.dtDateOfVaccination)
        winVaccineAddEdit.setTabOrder(self.dtDateOfVaccination, self.btnSave)

    def retranslateUi(self, winVaccineAddEdit):
        _translate = QtCore.QCoreApplication.translate
        winVaccineAddEdit.setWindowTitle(_translate("winVaccineAddEdit", "Add Vaccine"))
        self.lblDateOfAppointment.setText(_translate("winVaccineAddEdit", "Date of Appointment:"))
        self.dtDateOfAppointment.setDisplayFormat(_translate("winVaccineAddEdit", "dd MMMM yyyy"))
        self.dtDateOfVaccination.setDisplayFormat(_translate("winVaccineAddEdit", "dd MMMM yyyy"))
        self.lblDateOfVaccination.setText(_translate("winVaccineAddEdit", "Date of Vaccination:"))
        self.lblNameofVaccine.setText(_translate("winVaccineAddEdit", "Name of Vaccine:"))
        self.btnSave.setToolTip(_translate("winVaccineAddEdit", "Edit"))