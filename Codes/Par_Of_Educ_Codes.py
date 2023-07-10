from PyQt5.QtWidgets import QWidget, QAction, QMenu, QToolButton, QTableWidgetItem
from PyQt5 import QtGui
from Designs import Par_Of_Educ_Design
from Common_Codes import Common


class ParOfEduc(QWidget):
    def __init__(self):
        super().__init__()
        self.par_of_educ_win = Par_Of_Educ_Design.Ui_winParOfEduc()
        self.par_of_educ_win.setupUi(self)

    def settings(self):
        self.user = Common().fetch_user()
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;",
                                                     "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)

        options = ["All", "Still in Education", "Education Completed"]
        menu = QMenu()
        for option in options:
            action = QAction(option, menu)
            action.triggered.connect(self.set_option)
            menu.addAction(action)

        self.par_of_educ_win.toolbShow.setMenu(menu)
        self.par_of_educ_win.toolbShow.setPopupMode(QToolButton.InstantPopup)
        self.par_of_educ_win.tbwClients.setColumnHidden(0, True)
        self.par_of_educ_win.tbwClients.setColumnWidth(6, 120)
        self.par_of_educ_win.tbwClients.clicked.connect(self.fill_info)
        self.set_option()

    def set_option(self):
        if self.sender().text() != "Participants of Education":
            self.par_of_educ_win.toolbShow.setText(self.sender().text())

        if self.par_of_educ_win.toolbShow.text() == "All":
            query = f"SELECT * FROM view_clients WHERE PET_DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} ORDER BY FIRST_NAME;"
        elif self.par_of_educ_win.toolbShow.text() == "Still in Education":
            query = f"SELECT * FROM view_clients WHERE PET_DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} AND END_DATE IS NULL ORDER BY FIRST_NAME;"
        else:
            query = f"SELECT * FROM view_clients WHERE PET_DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} AND END_DATE IS NOT NULL ORDER BY FIRST_NAME;"
        clients = Common().db(query, "fetch")
        self.fill_tbw(clients)
        self.par_of_educ_win.lblNumber.setText(f"Number of Clients ({self.par_of_educ_win.toolbShow.text()}): "
                                               f"{self.par_of_educ_win.tbwClients.rowCount()}")

    def fetch_clients(self):
        query = f"SELECT * FROM view_clients WHERE PET_DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} ORDER BY FIRST_NAME;"
        clients = Common().db(query, "fetch")
        self.fill_tbw(clients)

    def fill_tbw(self, clients):
        self.par_of_educ_win.tbwClients.setRowCount(len(clients))
        for i in range(len(clients)):
            self.par_of_educ_win.tbwClients.setItem(i, 0, QTableWidgetItem(str(clients[i]["ID"])))
            self.par_of_educ_win.tbwClients.setItem(i, 1, QTableWidgetItem(clients[i]["TYPE_OF_CLIENT"]))
            self.par_of_educ_win.tbwClients.setItem(i, 2, QTableWidgetItem(clients[i]["COMPANY"]))
            self.par_of_educ_win.tbwClients.setItem(i, 3, QTableWidgetItem(clients[i]["FIRST_NAME"]))
            self.par_of_educ_win.tbwClients.setItem(i, 4, QTableWidgetItem(clients[i]["LAST_NAME"]))
            self.par_of_educ_win.tbwClients.setItem(i, 5, QTableWidgetItem(clients[i]["PET_NAME"]))
            self.par_of_educ_win.tbwClients.setItem(i, 6, QTableWidgetItem(clients[i]["TYPE_OF_EDUC"]))
            try:
                start_date = Common().date_format(str(clients[i]["START_DATE"]).split("-"))
            except:
                start_date = ""
            self.par_of_educ_win.tbwClients.setItem(i, 7, QTableWidgetItem(start_date))
            try:
                end_date = Common().date_format(str(clients[i]["END_DATE"]).split("-"))
            except:
                end_date = ""
            self.par_of_educ_win.tbwClients.setItem(i, 8, QTableWidgetItem(end_date))

    def fill_info(self):
        query = f"SELECT * FROM view_clients WHERE ID = {self.par_of_educ_win.tbwClients.item(self.par_of_educ_win.tbwClients.currentRow(), 0).text()}"
        client = Common().db(query, "fetch")[0]
        self.par_of_educ_win.entClientName.setText(f"{client['FIRST_NAME']} {client['LAST_NAME']}")
        self.par_of_educ_win.entCompany.setText(client["COMPANY"])
        self.par_of_educ_win.entCompanyPhone.setText(client["COMPANY_PHONE"])
        self.par_of_educ_win.entEMail.setText(client["MAIL"])
        self.par_of_educ_win.entAddress.setText(Common().address_format(client["ADDRESS"].split("---")))
        self.par_of_educ_win.entMobile.setText(client["MOBILE"])
        self.par_of_educ_win.entOtherPhones.setText(client["OTHER_PHONES"])
        self.par_of_educ_win.entReference.setText(client["REFERENCE"])
        ###############      I NEED view_clients FOR THE REST OF THESE:         #################
        # self.par_of_educ_win.entPetName.setText(client["PET_NAME"])
        # self.par_of_educ_win.dtDOB.setText(client["PET_DOB"])
        # self.par_of_educ_win.entGender.setText(client["GENDER"])
        # self.par_of_educ_win.entPetType.setText(client["TYPE"])
        # self.par_of_educ_win.entBreed.setText(client["BREED"])
        # self.par_of_educ_win.entColor.setText(client["COLOR"])
        # self.par_of_educ_win.entSpecialMark.setText(client["SPECIAL_MARK"])
