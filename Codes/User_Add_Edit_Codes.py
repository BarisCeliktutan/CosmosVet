from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import User_Add_Edit_Design
from Common_Codes import Common
from datetime import datetime


class UserAddEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.user_add_update_win = User_Add_Edit_Design.Ui_winUserAddEdit()
        self.user_add_update_win.setupUi(self)
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;",
                                                     "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.user_add_update_win.btnSave.clicked.connect(self.save)

        self.user_add_update_win.dtDOB.dateChanged.connect(lambda: Common().paint_dt(self.user_add_update_win.dtDOB))

        query = "SELECT user_name FROM users ORDER BY FIRST_NAME;"
        usernames_dict = Common().db(query, "fetch")
        self.usernames = []
        for username in usernames_dict:
            self.usernames.append(username["user_name"])

        self.user_add_update_win.toolbPhoneCodes.setMenu(Common().phone_codes(self.user_add_update_win.toolbPhoneCodes))
        self.user_add_update_win.toolbPhoneCodes.setPopupMode(QToolButton.InstantPopup)

    def add(self, clinic_id):
        self.clinic_id = clinic_id
        self.setWindowTitle("Add User")
        self.user_add_update_win.entFirstName.setText("")
        self.user_add_update_win.entLastName.setText("")
        self.user_add_update_win.entUserName.setText("")
        self.user_add_update_win.entPassword.setText("")
        self.user_add_update_win.entPasswordAgain.setText("")
        self.user_add_update_win.dtDOB.setDate(datetime.today())
        self.user_add_update_win.entAddress.setText("")
        self.user_add_update_win.entMail.setText("")
        self.user_add_update_win.toolbPhoneCodes.setText("...")
        self.user_add_update_win.entPhone.setText("")
        self.user_add_update_win.cbDr.setChecked(0)
        self.x = "add"
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def edit(self, editing):
        self.setWindowTitle("Edit User")
        self.editing = editing
        self.user_add_update_win.entFirstName.setText(editing["FIRST_NAME"])
        self.user_add_update_win.entLastName.setText(editing["LAST_NAME"])
        self.user_add_update_win.entUserName.setText(editing["USER_NAME"])
        self.user_add_update_win.entPassword.setText(editing["PASSWORD"])
        self.user_add_update_win.entPasswordAgain.setText(editing["PASSWORD"])
        self.user_add_update_win.dtDOB.setDate(editing["DOB"])
        self.user_add_update_win.entAddress.setText(editing["ADDRESS"])
        self.user_add_update_win.entMail.setText(editing["MAIL"])
        if len(editing["PHONE"]) != 0:
            self.user_add_update_win.toolbPhoneCodes.setText(editing["PHONE"][:3])
            self.user_add_update_win.entPhone.setText(editing["PHONE"][3:])
        else:
            self.user_add_update_win.entPhone.setText("")
            self.user_add_update_win.toolbPhoneCodes.setText("...")
        self.user_add_update_win.cbDr.setChecked(editing["VET_DR"])
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def save(self):
        first_name = self.user_add_update_win.entFirstName.text()
        last_name = self.user_add_update_win.entLastName.text()
        user_name = self.user_add_update_win.entUserName.text()
        password = self.user_add_update_win.entPassword.text()
        password_again = self.user_add_update_win.entPasswordAgain.text()
        date_of_birth = self.user_add_update_win.dtDOB.date().toPyDate()  # '{date_of_birth}'
        address = self.user_add_update_win.entAddress.text()
        mail = self.user_add_update_win.entMail.text()
        if self.user_add_update_win.toolbPhoneCodes.text() != "...":
            phone = f"{self.user_add_update_win.toolbPhoneCodes.text()}{self.user_add_update_win.entPhone.text()}"
        else:
            phone = ""
        vet_doctor = int(self.user_add_update_win.cbDr.isChecked())
        if first_name == "":
            Common().msg('Please enter the first name.')
        elif last_name == "":
            Common().msg('Please enter the last name.')
        elif user_name == "":
            Common().msg('Please enter the user name.')
        elif password == "":
            Common().msg('Please enter the password.')
        elif len(password) < 6:
            Common().msg('Password should be at least 6 characters.')
        elif password != password_again:
            Common().msg('Passwords does not match!')
        elif self.user_add_update_win.toolbPhoneCodes.text() == "..." and\
            len(self.user_add_update_win.entPhone.text()) > 9:
            Common().msg('Please select the phone code!')
        elif self.x == "add" and user_name in self.usernames or\
                self.x == "update" and user_name in self.usernames and user_name != self.editing["USER_NAME"]:
            Common().msg('This username has been used by another user. Please enter a different username.')
        else:
            sure = Common().save_msg()
            if sure == QMessageBox.Yes:
                if self.x == "add":
                    query = f"INSERT INTO users (FIRST_NAME, LAST_NAME, USER_NAME, PASSWORD, DOB, ADDRESS, MAIL," \
                        f"PHONE, VET_DR, CLINIC_ID) VALUES ('{first_name}', '{last_name}', '{user_name}'," \
                        f"'{password}', '{date_of_birth}', '{address}', '{mail}', " \
                        f"'{self.user_add_update_win.toolbPhoneCodes.text()}{phone}', {vet_doctor}," \
                        f"'{self.clinic_id}')"
                else:
                    query = f"UPDATE users SET FIRST_NAME = '{first_name}', LAST_NAME = '{last_name}'," \
                            f"USER_NAME = '{user_name}', PASSWORD = '{password}', DOB = '{date_of_birth}'," \
                            f"ADDRESS = '{address}', MAIL = '{mail}'," \
                            f"PHONE = '{phone}'," \
                            f"VET_DR = {vet_doctor} WHERE ID = {self.editing['ID']}"

                Common().db(query, 'commit')
                self.hide()
