from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import New_Vaccine_Design
from Common_Codes import Common
from datetime import datetime


class NewVaccine(QDialog):
    def __init__(self):
        super().__init__()
        self.new_vac_win = New_Vaccine_Design.Ui_winNewVaccine()
        self.new_vac_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.new_vac_win.btnSave.clicked.connect(self.save)

    def add(self, vac_id):
        self.vac_id = vac_id
        self.setWindowTitle("Add a New Vaccine")
        self.new_vac_win.entNameofVaccine.setText("")
        self.new_vac_win.entSerialNumber.setText("")
        self.new_vac_win.dtExpiryDate.setDate(datetime.today())
        self.new_vac_win.spinBoxQuantity.setValue(0)
        self.new_vac_win.spinBoxPeriod.setValue(0)
        self.setStyleSheet("background-color: rgb(150, 255, 84);")
        self.x = "add"

    def edit(self, editing):
        self.editing = editing
        self.setWindowTitle(f"Editing {editing['VACCINE_NAME']}")
        self.new_vac_win.entNameofVaccine.setText(editing["VACCINE_NAME"])
        self.new_vac_win.entSerialNumber.setText(editing["SERIAL_NUMBER"])
        self.new_vac_win.dtExpiryDate.setDate(editing["EXPIRY_DATE"])
        self.new_vac_win.spinBoxQuantity.setValue(int(editing["QUANTITY"]))
        self.new_vac_win.spinBoxPeriod.setValue(int(editing["PERIOD"]))
        self.setStyleSheet("background-color: rgb(255, 165, 0);")
        self.x = "edit"

    def save(self):
        vaccine_name = self.new_vac_win.entNameofVaccine.text()
        serial_number = self.new_vac_win.entSerialNumber.text()
        expiry_date = self.new_vac_win.dtExpiryDate.date().toPyDate()
        quantity = self.new_vac_win.spinBoxQuantity.value()
        period = self.new_vac_win.spinBoxPeriod.value()

        # clinic_id # db only (fetch bosses clinic id)

        sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to save?",
                           QMessageBox.Yes | QMessageBox.No).exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                query = f"INSERT INTO vaccine_types (VACCINE_NAME, SERIAL_NUMBER, EXPIRY_DATE, QUANTITY, PERIOD) "\
                        f"VALUES ('{vaccine_name}', '{serial_number}', '{expiry_date}', '{quantity}', " \
                        f"'{period}')"
            else:
                query = f"UPDATE vaccine_types SET VACCINE_NAME = '{vaccine_name}', SERIAL_NUMBER = '{serial_number}', "\
                        f"EXPIRY_DATE = '{expiry_date}', QUANTITY = '{quantity}', PERIOD = '{period}' " \
                        f"WHERE ID = {self.editing['ID']}"

            Common().db(query, 'commit')
            self.hide()