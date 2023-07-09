from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QMenu, QAction, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import Clients_And_Pets_Info_Design
from Codes import Client_Add_Edit_Code, Pet_Add_Edit_Code, Vaccines_Code, Vaccine_Add_Edit_Code, Charges_Code
from Common_Codes import Common
from datetime import datetime


class ClientsAndPetsInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.cl_pet_info_win = Clients_And_Pets_Info_Design.Ui_winClientsPetsInfo()
        self.cl_pet_info_win.setupUi(self)

    # def add(self, win):
    #     win.add()
    #     win.setModal(True)
    #     win.exec_()
    #     self.fetch_clients()

    # def edit(self, tbl, tbw, win, what):
    #     try:
    #         query = f"SELECT * FROM {tbl} WHERE ID ="\
    #                 f"{tbw.item(tbw.currentRow(), 0).text()};"
    #         editing = Common().db(query, "fetch")[0]
    #         win.edit(editing)
    #         win.setModal(True)
    #         win.exec_()
    #         self.fetch_clients()
    #         self.fill_cl_frm()
    #     except:
    #         QMessageBox.critical(self, "Warning", f"Please select a {what} first.")

    # def delete(self):
    #     try:
    #         sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to delete this client?",
    #                            QMessageBox.Yes | QMessageBox.No).exec_()
    #         if sure == QMessageBox.Yes:
    #             query = f"UPDATE CLIENTS SET DELETED = 1, DATE_OF_DELETE = '{datetime.today()}'" \
    #                     f" WHERE ID = {self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 0).text()}"
    #             Common().db(query, "commit")
    #             self.fetch_clients()
    #     except:
    #         QMessageBox.information(self, "Attention", "Please first select the client you want to delete.")

    def settings(self):
        self.user = Common().fetch_user()

        self.cl_pet_info_win.tbwClients.setColumnHidden(0, True)
        self.cl_pet_info_win.tbwClients.setColumnWidth(1, 183)
        self.cl_pet_info_win.tbwClients.setColumnWidth(2, 130)
        self.cl_pet_info_win.tbwClients.setColumnWidth(3, 130)

        self.cl_pet_info_win.tbwPets.setColumnHidden(0, True)
        self.cl_pet_info_win.tbwPets.setColumnWidth(1, 183)
        self.cl_pet_info_win.tbwPets.setColumnWidth(2, 130)
        self.cl_pet_info_win.tbwPets.setColumnWidth(3, 130)

        self.cl_pet_info_win.tbwVaccines.setColumnHidden(0, True)
        self.cl_pet_info_win.tbwVaccines.setColumnWidth(1, 230)
        self.cl_pet_info_win.tbwVaccines.setColumnWidth(2, 170)
        self.cl_pet_info_win.tbwVaccines.setColumnWidth(3, 140)

        self.cl_add_edit_window = Client_Add_Edit_Code.ClientAddEdit()
        self.pet_add_edit_window = Pet_Add_Edit_Code.PetAddEdit()
        self.vaccines_window = Vaccines_Code.Vaccines()
        self.vaccine_add_edit_window = Vaccine_Add_Edit_Code.VaccineAddEdit()
        self.charges_window = Charges_Code.Charges()

        self.cl_pet_info_win.btnClientAdd.clicked.connect(lambda: Common().add(self.cl_add_edit_window, self.fetch_clients, self.user["CLINIC_ID"], ""))
        self.cl_pet_info_win.btnClientEdit.clicked.connect(lambda: Common().edit(self.cl_pet_info_win.tbwClients, self.cl_add_edit_window, "clients", self.fetch_clients))
        self.cl_pet_info_win.btnClientDelete.clicked.connect(lambda: Common().delete(self.cl_pet_info_win.tbwClients, "clients", self.fetch_clients, self.fetch_pets))

        self.cl_pet_info_win.btnPetAdd.clicked.connect(lambda: self.fetch_id(self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 0), self.pet_add_edit_window, self.fetch_pets, "client"))
        self.cl_pet_info_win.btnPetEdit.clicked.connect(lambda: Common().edit(self.cl_pet_info_win.tbwPets, self.pet_add_edit_window, "pets", self.fetch_pets))
        self.cl_pet_info_win.btnPetDelete.clicked.connect(lambda: Common().delete(self.cl_pet_info_win.tbwPets, "pets", self.fetch_pets, ""))

        self.cl_pet_info_win.btnVaccines.clicked.connect(lambda: self.fetch_id(self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0), self.vaccines_window, self.fetch_vaccines, "pet"))
        self.cl_pet_info_win.btnVaccineEdit.clicked.connect(lambda: Common().edit(self.cl_pet_info_win.tbwVaccines, self.vaccine_add_edit_window, "vaccines", self.fetch_vaccines))
        self.cl_pet_info_win.btnVaccineDelete.clicked.connect(lambda: Common().delete(self.cl_pet_info_win.tbwVaccines, "vaccines", self.fetch_vaccines, ""))

        self.cl_pet_info_win.tbwClients.clicked.connect(self.fill_cl_frm)
        self.cl_pet_info_win.entCompanyName.textChanged.connect(self.finder)
        self.cl_pet_info_win.entFirstName.textChanged.connect(self.finder)
        self.cl_pet_info_win.entLastName.textChanged.connect(self.finder)
        self.cl_pet_info_win.btnClear.clicked.connect(self.clear)
        self.cl_pet_info_win.tbwPets.clicked.connect(self.fill_pets_frm)

        self.cl_pet_info_win.btnCharges.clicked.connect(self.charges)

        options = ["All", "Coming Appointments", "Past Appointments"]
        menu = QMenu()
        for option in options:
            action = QAction(option, menu)
            action.triggered.connect(self.set_option)
            menu.addAction(action)

        self.cl_pet_info_win.toolbShow.setMenu(menu)
        self.cl_pet_info_win.toolbShow.setPopupMode(QToolButton.InstantPopup)
        self.cl_pet_info_win.lblShow.setHidden(True)
        self.cl_pet_info_win.toolbShow.setHidden(True)

    def fetch_id(self, tbw, win, fetch, what):
        try:
            cl_id = [tbw.text(), self.user['CLINIC_ID']]
            Common().add(win, fetch, cl_id, what)
        except:
            Common().msg(f"Please first select a {what}.")

    def fetch_clients(self):
        query = f"SELECT * FROM clients WHERE DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} ORDER BY FIRST_NAME;"
        self.clients = Common().db(query, "fetch")
        self.fill_cl(self.clients)

    def fetch_pets(self):
        try:
            pets_query = f"SELECT * FROM pets WHERE DELETED = 0 AND CLIENT_ID = {self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 0).text()} ORDER BY NAME;"
            self.pets = Common().db(pets_query, "fetch")
            self.fill_pets(self.pets)
            self.fill_pets_frm()
        except:
            print("Not any client selected")

    def fetch_vaccines(self):
        try:
            vaccines_query = f"SELECT * FROM vaccines WHERE DELETED = 0 AND PET_ID = {self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0).text()} ORDER BY VACCINE_NAME;"
            vaccines = Common().db(vaccines_query, "fetch")
        except:
            vaccines = []
        self.fill_vaccines(vaccines)

    def finder(self):
        try:
            company_name = self.cl_pet_info_win.entCompanyName.text()
            first_name = self.cl_pet_info_win.entFirstName.text()
            last_name = self.cl_pet_info_win.entLastName.text()
            query = f"SELECT * FROM clients WHERE COMPANY LIKE '%{company_name}%' AND FIRST_NAME LIKE " \
                f"'%{first_name}%' AND LAST_NAME LIKE '%{last_name}%' AND DELETED = '0' ORDER BY FIRST_NAME;"

            clients = Common().db(query, "fetch")
            self.fill_cl(clients)
        except:
            print("No Data Found!")

    def clear(self):
        self.cl_pet_info_win.entCompanyName.setText("")
        self.cl_pet_info_win.entFirstName.setText("")
        self.cl_pet_info_win.entLastName.setText("")
        self.finder()

    def fill_cl(self, clients):
        self.cl_pet_info_win.tbwClients.setRowCount(len(clients))
        for row, client in enumerate(clients):
            self.cl_pet_info_win.tbwClients.setItem(row, 0, QTableWidgetItem(str(client["ID"])))
            self.cl_pet_info_win.tbwClients.setItem(row, 1, QTableWidgetItem(client["COMPANY"]))
            self.cl_pet_info_win.tbwClients.setItem(row, 2, QTableWidgetItem(client["FIRST_NAME"]))
            self.cl_pet_info_win.tbwClients.setItem(row, 3, QTableWidgetItem(client["LAST_NAME"]))
        Common().set_number_of(self.cl_pet_info_win.tbwClients, self.cl_pet_info_win.lblNumberofCl, "Clients")
        self.show_options(0)

    def fill_pets(self, pets):
        self.show_options(0)
        self.cl_pet_info_win.tbwPets.setRowCount(len(pets))
        for row, pet in enumerate(pets):
            self.cl_pet_info_win.tbwPets.setItem(row, 0, QTableWidgetItem(str(pet["ID"])))
            date_of_entry = Common().date_format(str(pet["DATE_OF_ENTRY"]).split("-"))
            self.cl_pet_info_win.tbwPets.setItem(row, 1, QTableWidgetItem(date_of_entry))
            self.cl_pet_info_win.tbwPets.setItem(row, 2, QTableWidgetItem(pet["NAME"]))
            self.cl_pet_info_win.tbwPets.setItem(row, 3, QTableWidgetItem(pet["TYPE"]))
        Common().set_number_of(self.cl_pet_info_win.tbwPets, self.cl_pet_info_win.lblNumberofPets, "Pets")

    def fill_vaccines(self, vaccines):
        self.cl_pet_info_win.tbwVaccines.setRowCount(len(vaccines))
        self.show_options(len(vaccines))
        for row, vaccine in enumerate(vaccines):
            self.cl_pet_info_win.tbwVaccines.setItem(row, 0, QTableWidgetItem(str(vaccine["ID"])))
            self.cl_pet_info_win.tbwVaccines.setItem(row, 1, QTableWidgetItem(vaccine["VACCINE_NAME"]))
            try:
                date_of_appointment = Common().date_format(str(vaccine["DATE_OF_APPOINTMENT"]).split("-"))
                self.cl_pet_info_win.tbwVaccines.setItem(row, 2, QTableWidgetItem(date_of_appointment))
            except:
                self.cl_pet_info_win.tbwVaccines.setItem(row, 2, QTableWidgetItem(""))
            try:
                date_of_vaccined = Common().date_format(str(vaccine["DATE_OF_VACCINED"]).split("-"))
                self.cl_pet_info_win.tbwVaccines.setItem(row, 3, QTableWidgetItem(date_of_vaccined))
            except:
                self.cl_pet_info_win.tbwVaccines.setItem(row, 3, QTableWidgetItem(""))

    def fill_cl_frm(self):
        # self.cl_pet_info_win.dtBirthday.setDate(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["DOB"]) ## DATE OF LAST VISIT?
        self.cl_pet_info_win.dtEntry.setDate(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["DATE_OF_ENTRY"])
        self.cl_pet_info_win.entTypeOfClient.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["TYPE_OF_CLIENT"])
        self.cl_pet_info_win.entAddress.setText(Common().address_format(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["ADDRESS"].split("---")))
        self.cl_pet_info_win.entMail.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["MAIL"])
        self.cl_pet_info_win.entReference.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["REFERENCE"])
        self.cl_pet_info_win.dtBirthday.setDate(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["DOB"])
        self.cl_pet_info_win.entMobile.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["MOBILE"])
        self.cl_pet_info_win.entCompanyPhone.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["COMPANY_PHONE"])
        self.cl_pet_info_win.entOtherPhones.setText(self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["OTHER_PHONES"])
        self.cl_pet_info_win.entChargesLeft.setText(f' £ {self.clients[self.cl_pet_info_win.tbwClients.currentRow()]["CHARGES_LEFT"]}')
        self.fetch_pets()
        Common().set_number_of(self.cl_pet_info_win.tbwPets, self.cl_pet_info_win.lblNumberofPets, "Pets")

    def fill_pets_frm(self):
        if self.cl_pet_info_win.tbwPets.currentRow() > -1:
            # self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0).text()
            self.cl_pet_info_win.entChipNo.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["CHIP_NO"])
            self.cl_pet_info_win.entName.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["NAME"])
            self.cl_pet_info_win.dtDOB.setDate(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["DOB"])
            self.cl_pet_info_win.entType.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["TYPE"])
            self.cl_pet_info_win.entGender.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["GENDER"])
            self.cl_pet_info_win.entBreed.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["BREED"])
            self.cl_pet_info_win.entColor.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["COLOR"])
            self.cl_pet_info_win.entSpecialMark.setText(self.pets[self.cl_pet_info_win.tbwPets.currentRow()]["SPECIAL_MARK"])
        else:
            self.cl_pet_info_win.entChipNo.setText("")
            self.cl_pet_info_win.entName.setText("")
            self.cl_pet_info_win.dtDOB.setDate(datetime.today())
            self.cl_pet_info_win.entType.setText("")
            self.cl_pet_info_win.entGender.setText("")
            self.cl_pet_info_win.entBreed.setText("")
            self.cl_pet_info_win.entColor.setText("")
            self.cl_pet_info_win.entSpecialMark.setText("")
        self.fetch_vaccines()

    def set_option(self):
        self.cl_pet_info_win.toolbShow.setText(self.sender().text())

        if self.cl_pet_info_win.toolbShow.text() == "All":
            vaccines_query = f"SELECT * FROM vaccines WHERE DELETED = 0 AND PET_ID = {self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0).text()} ORDER BY VACCINE_NAME;"
        elif self.cl_pet_info_win.toolbShow.text() == "Coming Appointments":
            vaccines_query = f"SELECT * FROM vaccines WHERE DELETED = 0 AND PET_ID = {self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0).text()} AND DATE_OF_APPOINTMENT >= CURRENT_DATE AND DATE_OF_VACCINED IS NULL ORDER BY VACCINE_NAME;"
        else:
            vaccines_query = f"SELECT * FROM vaccines WHERE DELETED = 0 AND PET_ID = {self.cl_pet_info_win.tbwPets.item(self.cl_pet_info_win.tbwPets.currentRow(), 0).text()}  AND DATE_OF_VACCINED IS NOT NULL ORDER BY VACCINE_NAME;"
        vaccines = Common().db(vaccines_query, "fetch")
        self.fill_vaccines(vaccines)

    def show_options(self, isGreater):
        if isGreater > 0:
            self.cl_pet_info_win.lblShow.setHidden(False)
            self.cl_pet_info_win.toolbShow.setHidden(False)
        else:
            self.cl_pet_info_win.lblShow.setHidden(True)
            self.cl_pet_info_win.toolbShow.setHidden(True)

    def charges(self):
        try:
            self.charges_window.settings(self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 0).text(),
                                         f"{self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 2).text()} "
                                         f"{self.cl_pet_info_win.tbwClients.item(self.cl_pet_info_win.tbwClients.currentRow(), 3).text()}")
            self.charges_window.setModal(True)
            self.charges_window.exec_()
            self.fetch_clients()
            self.fill_cl_frm()
        except:
            Common().msg("Please first select a client.")
