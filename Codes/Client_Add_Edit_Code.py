from PyQt5.QtWidgets import QDialog, QMessageBox, QToolButton
from PyQt5 import QtCore
from Designs import Client_Add_Edit_Design
from Common_Codes import Common
from datetime import datetime


class ClientAddEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.cl_add_edit_win = Client_Add_Edit_Design.Ui_winClientAddEdit()
        self.cl_add_edit_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.cl_add_edit_win.dtDOB.dateChanged.connect(lambda: Common().paint_dt(self.cl_add_edit_win.dtDOB))
        self.cl_add_edit_win.dtWedAnn.dateChanged.connect(lambda: Common().paint_dt(self.cl_add_edit_win.dtWedAnn))
        self.cl_add_edit_win.toolbPhoneCodes.setMenu(Common().phone_codes(self.cl_add_edit_win.toolbPhoneCodes))
        self.cl_add_edit_win.toolbPhoneCodes.setPopupMode(QToolButton.InstantPopup)
        self.cl_add_edit_win.btnSave.clicked.connect(self.save)

    def add(self, clinic_id):
        self.clinic_id = clinic_id
        self.setWindowTitle("Add Client")
        self.cl_add_edit_win.dtDateOfEntry.setDate(datetime.today())
        self.cl_add_edit_win.entFirstName.setText("")
        self.cl_add_edit_win.entLastName.setText("")
        self.cl_add_edit_win.toolbPhoneCodes.setText("...")
        self.cl_add_edit_win.entPhone.setText("")
        self.cl_add_edit_win.entTypeOfClient.setText("")
        self.cl_add_edit_win.entCompanyName.setText("")
        self.cl_add_edit_win.entAddressLn1.setText("")
        self.cl_add_edit_win.entAddressLn2.setText("")
        self.cl_add_edit_win.entCityTown.setText("")
        self.cl_add_edit_win.entPostcode.setText("")
        self.cl_add_edit_win.entCompanyPhone.setText("")
        self.cl_add_edit_win.entOtherPhones.setText("")
        self.cl_add_edit_win.entMail.setText("")
        self.cl_add_edit_win.entReference.setText("")
        self.cl_add_edit_win.dtDOB.setDate(datetime.today())
        self.cl_add_edit_win.dtWedAnn.setDate(datetime.today())
        self.cl_add_edit_win.entOccupation.setText("")
        self.cl_add_edit_win.cbActive.setChecked(0)
        self.x = "add"
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def edit(self, editing):
        self.setWindowTitle(f"Editing {editing['FIRST_NAME']} {editing['LAST_NAME']}")
        self.editing = editing
        self.cl_add_edit_win.dtDateOfEntry.setDate(editing["DATE_OF_ENTRY"])
        self.cl_add_edit_win.entFirstName.setText(editing["FIRST_NAME"])
        self.cl_add_edit_win.entLastName.setText(editing["LAST_NAME"])
        if len(editing["MOBILE"]) != 0:
            self.cl_add_edit_win.toolbPhoneCodes.setText(editing["MOBILE"][:3])
            self.cl_add_edit_win.entPhone.setText(editing["MOBILE"][3:])
        else:
            self.cl_add_edit_win.entPhone.setText("")
            self.cl_add_edit_win.toolbPhoneCodes.setText("...")
        self.cl_add_edit_win.entTypeOfClient.setText(editing["TYPE_OF_CLIENT"])
        self.cl_add_edit_win.entCompanyName.setText(editing["COMPANY"])
        self.cl_add_edit_win.entAddressLn1.setText(editing["ADDRESS"].split("---")[0])
        self.cl_add_edit_win.entAddressLn2.setText(editing["ADDRESS"].split("---")[1])
        self.cl_add_edit_win.entCityTown.setText(editing["ADDRESS"].split("---")[2])
        self.cl_add_edit_win.entPostcode.setText(editing["ADDRESS"].split("---")[3])
        self.cl_add_edit_win.entCompanyPhone.setText(editing["COMPANY_PHONE"])
        self.cl_add_edit_win.entOtherPhones.setText(editing["OTHER_PHONES"])
        self.cl_add_edit_win.entMail.setText(editing["MAIL"])
        self.cl_add_edit_win.entReference.setText(editing["REFERENCE"])
        self.cl_add_edit_win.dtDOB.setDate(editing["DOB"])
        self.cl_add_edit_win.dtWedAnn.setDate(editing["WED_ANN"])
        self.cl_add_edit_win.entOccupation.setText(editing["OCCUPATION"])
        self.cl_add_edit_win.cbActive.setChecked(editing["ACTIVE"])
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def save(self):
        date_of_entry = self.cl_add_edit_win.dtDateOfEntry.date().toPyDate()
        first_name = self.cl_add_edit_win.entFirstName.text()
        last_name = self.cl_add_edit_win.entLastName.text()
        if self.cl_add_edit_win.toolbPhoneCodes.text() != "...":
            phone = f"{self.cl_add_edit_win.toolbPhoneCodes.text()}{self.cl_add_edit_win.entPhone.text()}"
        else:
            phone = ""
        type_of_client = self.cl_add_edit_win.entTypeOfClient.text()
        company_name = self.cl_add_edit_win.entCompanyName.text()
        address = f"{self.cl_add_edit_win.entAddressLn1.text()}---{self.cl_add_edit_win.entAddressLn2.text()}" \
                  f"---{self.cl_add_edit_win.entCityTown.text()}---{self.cl_add_edit_win.entPostcode.text()}"
        company_phone = self.cl_add_edit_win.entCompanyPhone.text()
        other_phones = self.cl_add_edit_win.entOtherPhones.toPlainText()
        mail = self.cl_add_edit_win.entMail.text()
        reference = self.cl_add_edit_win.entReference.text()
        dob = self.cl_add_edit_win.dtDOB.date().toPyDate()
        wed_ann = self.cl_add_edit_win.dtWedAnn.date().toPyDate()
        occupation = self.cl_add_edit_win.entOccupation.text()
        active = int(self.cl_add_edit_win.cbActive.isChecked())

        # clinic_id # db only (fetch bosses clinic id)
        sure = Common().save_msg().exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                query = f"INSERT INTO clients (DATE_OF_ENTRY, FIRST_NAME, LAST_NAME, MOBILE, TYPE_OF_CLIENT, COMPANY,"\
                        f"ADDRESS, COMPANY_PHONE, OTHER_PHONES, MAIL, REFERENCE, DOB, WED_ANN, OCCUPATION, ACTIVE,"\
                        f"CLINIC_ID) VALUES ('{date_of_entry}', '{first_name}', '{last_name}', '{phone}',"\
                        f"'{type_of_client}', '{company_name}', '{address}', '{company_phone}', '{other_phones}',"\
                        f"'{mail}', '{reference}', '{dob}', '{wed_ann}', '{occupation}', {active}," \
                        f"{self.clinic_id})"
            else:
                query = f"UPDATE clients SET DATE_OF_ENTRY = '{date_of_entry}', FIRST_NAME = '{first_name}', " \
                        f"LAST_NAME = '{last_name}', MOBILE = '{phone}', TYPE_OF_CLIENT = '{type_of_client}', " \
                        f"COMPANY = '{company_name}', ADDRESS = '{address}', COMPANY_PHONE = '{company_phone}', " \
                        f"OTHER_PHONES = '{other_phones}', MAIL = '{mail}', REFERENCE = '{reference}', DOB = '{dob}', "\
                        f"WED_ANN = '{wed_ann}', OCCUPATION = '{occupation}', ACTIVE = {active} " \
                        f"WHERE ID = {self.editing['ID']}"

            Common().db(query, 'commit')
            self.hide()
