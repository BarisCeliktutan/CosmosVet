from PyQt5.QtWidgets import QWidget, QMessageBox, QAction, QMenu, QToolButton, QTableWidgetItem
from PyQt5 import QtCore, QtGui
from Designs import Par_Of_Educ_Design
from Common_Codes import Common
from datetime import datetime


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

    def set_option(self):
        self.par_of_educ_win.toolbShow.setText(self.sender().text())
        self.par_of_educ_win.lblNumber.setText(f"Number of Clients ({self.sender().text()}): "
                                               f"{self.par_of_educ_win.tbwClients.rowCount()}")
        if self.sender().text() == "All":
            query = f"SELECT * FROM clients WHERE DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} ORDER BY FIRST_NAME;"
        elif self.sender().text() == "Still in Education":
            query = f"SELECT * FROM clients WHERE DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} AND END_DATE IS NULL ORDER BY FIRST_NAME;"
        elif self.sender().text() == "Education Completed":
            query = f"SELECT * FROM clients WHERE DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} AND END_DATE IS NOT NULL ORDER BY FIRST_NAME;"
        clients = Common().db(query, "fetch")
        self.fill_tbw(clients)

    def fetch_clients(self):
        query = f"SELECT * FROM clients WHERE DELETED = 0 AND CLINIC_ID = {self.user['CLINIC_ID']} ORDER BY FIRST_NAME;"
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
