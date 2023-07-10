from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore
from Designs import Vaccine_Add_Edit_Design
from Codes import Vaccines_Code
from Common_Codes import Common
from datetime import datetime


class VaccineAddEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.vac_add_edit_win = Vaccine_Add_Edit_Design.Ui_winVaccineAddEdit()
        self.vac_add_edit_win.setupUi(self)

        self.vaccines_window = Vaccines_Code.Vaccines()
        self.vac_add_edit_win.dtDateOfVaccination.setEnabled(False)

        self.vac_add_edit_win.btnNameofVaccine.clicked.connect(self.vaccine_name)
        self.vac_add_edit_win.cbDateOfVaccination.stateChanged.connect(self.checked)
        self.vac_add_edit_win.btnSave.clicked.connect(self.save)

    def add(self, ids):
        self.pet_id = ids[0]
        self.cl_id = ids[1]
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
            self.vac_add_edit_win.cbDateOfVaccination.setChecked(True)
        except:
            self.vac_add_edit_win.cbDateOfVaccination.setChecked(False)
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def vaccine_name(self):
        if self.x == "edit":
            self.vaccines_window.settings(self.editing["CLINIC_ID"])
        else:
            self.vaccines_window.settings(self.cl_id)
        self.vaccines_window.setModal(True)
        self.vaccines_window.exec_()
        try:
            self.vaccine_id, self.vaccine_name, flag = self.vaccines_window.fill_vaccine_name()
            if flag:
                self.vac_add_edit_win.entNameofVaccine.setText(self.vaccine_name)
        except:
            print("closed without selecting any")

    def checked(self):
        if self.vac_add_edit_win.cbDateOfVaccination.checkState() == QtCore.Qt.Checked:
            self.vac_add_edit_win.dtDateOfVaccination.setEnabled(True)
            bg = "background-color: rgb(255, 255, 255);"
        else:
            self.vac_add_edit_win.dtDateOfVaccination.setEnabled(False)
            bg = "background-color: rgb(232, 232, 232);"
        self.vac_add_edit_win.cbDateOfVaccination.setStyleSheet(bg)
        self.vac_add_edit_win.dtDateOfVaccination.setStyleSheet(bg)

    def save(self):
        name_of_vaccine = self.vac_add_edit_win.entNameofVaccine.text()
        date_of_appointment = self.vac_add_edit_win.dtDateOfAppointment.date().toPyDate()
        if self.vac_add_edit_win.cbDateOfVaccination.isChecked():
            date_of_vaccination = f"'{self.vac_add_edit_win.dtDateOfVaccination.date().toPyDate()}'"
        else:
            date_of_vaccination = "NULL"

        # clinic_id # db only (fetch bosses clinic id)
        sure = Common().save_msg().exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                query = f"INSERT INTO vaccines (VACCINE_NAME, DATE_OF_APPOINTMENT, DATE_OF_VACCINED, PET_ID) VALUES "\
                        f"('{name_of_vaccine}', '{date_of_appointment}', {date_of_vaccination}, {self.pet_id})"
            else:
                query = f"UPDATE vaccines SET VACCINE_NAME = '{name_of_vaccine}', DATE_OF_APPOINTMENT = "\
                        f"'{date_of_appointment}', DATE_OF_VACCINED = {date_of_vaccination} " \
                        f"WHERE ID = {self.editing['ID']}"

            Common().db(query, 'commit')
            self.hide()
