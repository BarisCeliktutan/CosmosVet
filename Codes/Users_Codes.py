from PyQt5.QtWidgets import QWidget, QMessageBox, QCheckBox, QTableWidgetItem
from PyQt5 import QtCore, QtGui
from Designs import Users_Design
from Codes import User_Add_Edit_Codes
from Common_Codes import Common
from datetime import datetime


class Users(QWidget):
    def __init__(self):
        super().__init__()
        self.users_win = Users_Design.Ui_winUsers()
        self.users_win.setupUi(self)

    def settings(self):
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;",
                                                     "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)
        self.user_add_update_window = User_Add_Edit_Codes.UserAddEdit()
        self.users_win.btnAdd.clicked.connect(lambda: Common().add(self.user_add_update_window, self.fill_users, Common().fetch_user()["ID"], ""))
        self.users_win.btnEdit.clicked.connect(lambda: Common().edit(self.users_win.tbwUsers, self.user_add_update_window, "users", self.fill_users))
        self.users_win.btnDelete.clicked.connect(lambda: Common().delete(self.users_win.tbwUsers, "users", self.fill_users, ""))
        # self.users_win.btnDelete.clicked.connect(self.user_delete)

        self.users_win.tbwUsers.setColumnHidden(0, True)
        self.users_win.tbwUsers.setColumnWidth(1, 95)
        self.users_win.tbwUsers.setColumnWidth(2, 120)
        self.users_win.tbwUsers.setColumnWidth(3, 120)
        self.users_win.tbwUsers.setColumnWidth(4, 100)
        self.users_win.tbwUsers.setColumnWidth(5, 200)
        self.users_win.tbwUsers.setColumnWidth(6, 150)
        self.users_win.tbwUsers.setColumnWidth(7, 150)
        self.users_win.tbwUsers.setColumnWidth(8, 110)

    def fill_users(self):
        users_query = "SELECT * FROM users WHERE DELETED = 0;"
        self.users = Common().db(users_query, "fetch")
        self.users_win.tbwUsers.setRowCount(len(self.users))
        for i in range(len(self.users)):
            cb = QCheckBox()
            cb.setChecked(self.users[i]["VET_DR"])
            cb.stateChanged.connect(self.cb_update)
            cb.setStyleSheet("QCheckBox { margin-left: auto; margin-right: auto; }")
            self.users_win.tbwUsers.setCellWidget(i, 1, cb)

            # item.setAlignment(QtCore.Qt.AlignCenter)

            self.users_win.tbwUsers.setItem(i, 0, QTableWidgetItem(str(self.users[i]["ID"])))
            self.users_win.tbwUsers.setItem(i, 2, QTableWidgetItem(str(self.users[i]["FIRST_NAME"])))
            self.users_win.tbwUsers.setItem(i, 3, QTableWidgetItem(str(self.users[i]["LAST_NAME"])))
            self.users_win.tbwUsers.setItem(i, 4, QTableWidgetItem(str(self.users[i]["USER_NAME"])))
            self.users_win.tbwUsers.setItem(i, 5, QTableWidgetItem(str(self.users[i]["MAIL"])))
            self.users_win.tbwUsers.setItem(i, 6, QTableWidgetItem(str(self.users[i]["PHONE"])))
            self.users_win.tbwUsers.setItem(i, 7, QTableWidgetItem(str(self.users[i]["ADDRESS"])))
            date = Common().date_format(str(self.users[i]["DOB"]).split("-"))
            self.users_win.tbwUsers.setItem(i, 8, QTableWidgetItem(date))

    def cb_update(self):
        query = f"UPDATE users SET VET_DR = {int(self.sender().isChecked())} WHERE ID = {self.users[0]['ID']};"
        Common().db(query, "commit")

    # def user_add(self):
    #     self.user_add_update_window.user_add()
    #     self.user_add_update_window.setModal(True)
    #     self.user_add_update_window.exec_()
    #     self.fill_users()

    # def user_edit(self):
    #     try:
    #         query = f"SELECT * FROM users WHERE ID ="\
    #                 f"{self.users_win.tbwUsers.item(self.users_win.tbwUsers.currentRow(), 0).text()};"
    #         editing = Common().db(query, "fetch")[0]
    #         self.user_add_update_window.user_edit(editing)
    #         self.user_add_update_window.setModal(True)
    #         self.user_add_update_window.exec_()
    #         self.fill_users()
    #     except:
    #         QMessageBox.critical(self, "Warning", "Please select a user first.")

    # def user_delete(self):
    #     try:
    #         sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to save?",
    #                            QMessageBox.Yes | QMessageBox.No).exec_()
    #         if sure == QMessageBox.Yes:
    #             query = f"UPDATE users SET DELETED = 1, DATE_OF_DELETE = '{datetime.today()}'" \
    #                     f" WHERE ID = {self.users_win.tbwUsers.item(self.users_win.tbwUsers.currentRow(), 0).text()}"
    #             Common().db(query, "commit")
    #             self.fill_users()
    #     except:
    #         QMessageBox.information(self, "Attention", "Please first select the user you want to delete.")
