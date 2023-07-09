from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import Vaccine_Add_Edit_Design
from Common_Codes import Common
from datetime import datetime


class VaccineAddEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.vac_add_edit_win = Vaccine_Add_Edit_Design.Ui_winVaccineAddEdit()
        self.vac_add_edit_win.setupUi(self)

        self.vac_add_edit_win.btnSave.clicked.connect(self.save)

    def add(self, pet_id):
        self.pet_id = pet_id
        self.setWindowTitle("Add Vaccine to this pet") ## fetch also the name of pet!
        self.vac_add_edit_win.entNameofVaccine.setText("")
        self.vac_add_edit_win.dtDateOfAppointment.setDate(datetime.today())
        self.vac_add_edit_win.dtDateOfVaccination.setDate(datetime.today())
        self.x = "add"
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def edit(self, editing):
        self.editing = editing
        self.setWindowTitle("Edit this vaccination") ## fetch also the name of pet!
        self.vac_add_edit_win.entNameofVaccine.setText(editing["VACCINE_NAME"])
        try:
            self.vac_add_edit_win.dtDateOfAppointment.setDate(editing["DATE_OF_APPOINTMENT"])
        except:
            pass
        try:
            self.vac_add_edit_win.dtDateOfVaccination.setDate(editing["DATE_OF_VACCINED"])
        except:
            pass
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def save(self):
        name_of_vaccine = self.vac_add_edit_win.entNameofVaccine.text()
        date_of_appointment = self.vac_add_edit_win.dtDateOfAppointment.date().toPyDate()
        date_of_vaccination = self.vac_add_edit_win.dtDateOfVaccination.date().toPyDate()

        # clinic_id # db only (fetch bosses clinic id)
        sure = Common().save_msg().exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                query = f"INSERT INTO vaccines (VACCINE_NAME, DATE_OF_APPOINTMENT, DATE_OF_VACCINED, PET_ID) VALUES "\
                        f"('{name_of_vaccine}', '{date_of_appointment}', '{date_of_vaccination}', {self.pet_id})"
            else:
                query = f"UPDATE vaccines SET VACCINE_NAME = '{name_of_vaccine}', DATE_OF_APPOINTMENT = "\
                        f"'{date_of_appointment}', DATE_OF_VACCINED = '{date_of_vaccination}' " \
                        f"WHERE ID = {self.editing['ID']}"

            Common().db(query, 'commit')
            self.hide()
