from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from Designs import Login_Design
from Codes import Main_Win_Code, Reminder_Code
from Common_Codes import Common
from getmac import get_mac_address
from datetime import datetime


class LoginWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_win = Login_Design.Ui_winLogin()
        self.login_win.setupUi(self)
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;", "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)
        self.flag = 0

        self.reminder_window = Reminder_Code.Reminder()

        self.main_window = Main_Win_Code.MainWin()
        self.login_win.btnLogin.clicked.connect(self.login)
        self.mac = get_mac_address(interface="WiFi")
        try:
            remember_query = f"SELECT * FROM users WHERE MAC LIKE '%{self.mac}%' AND LAST_LOGIN = 1;"
            self.user = Common().db(remember_query, "fetch")[0]
            self.flag = 1
            self.login_win.cbRememberMe.setChecked(self.user["REMEMBER_ME"])
            if self.login_win.cbRememberMe.isChecked():
                self.login_win.entUserName.setText(self.user["USER_NAME"])
                self.login_win.entPassword.setText(self.user["PASSWORD"])
        except:
            self.user = ""

    def login(self):
        user_name = self.login_win.entUserName.text()
        password = self.login_win.entPassword.text()
        try:
            user_query = f"SELECT * FROM users WHERE USER_NAME = '{user_name}' AND PASSWORD = '{password}'"
            self.user = Common().db(user_query, "fetch")[0]
            mac_code = ""
            if self.flag == 0:
                if self.mac not in str(self.user['MAC'].split(",")):
                    if len(self.user["MAC"]) > 0:
                        mac_code = f", MAC = '{self.user['MAC']}, {self.mac}'"
                    else:
                        mac_code = f", MAC = '{self.mac}'"

            reminder = ""
            if self.user["REMIND_DATE"] < datetime.today().date():
                reminder = f", REMIND = 1, REMIND_DATE = '{datetime.today().date()}'"

            query = f"UPDATE users SET REMEMBER_ME = {self.login_win.cbRememberMe.isChecked()}{mac_code}, " \
                    f"LAST_LOGIN = 1{reminder} WHERE ID = '{self.user['ID']}' AND MAC LIKE '%{self.user['MAC']}%'"
            Common().db(query, "commit")

            last_login_query = f"UPDATE users SET LAST_LOGIN = 0 WHERE MAC LIKE '%{self.mac}%' AND USER_NAME <> '{user_name}';"
            Common().db(last_login_query, "commit")
            Common().user_info(self.user)
            self.main_window.settings()
            self.main_window.show()

            appointment_check_query = f"SELECT ID, FIRST_NAME, LAST_NAME, PET_NAME, VACCINE_NAME, DATE_OF_APPOINTMENT "\
                                      f"FROM view_clients WHERE CLINIC_ID = {self.user['CLINIC_ID']} "\
                                      f"AND DATE_OF_APPOINTMENT > CURDATE() AND DATE_OF_APPOINTMENT" \
                                      f"<= DATE_ADD(CURDATE(), INTERVAL 7 DAY) AND DATE_OF_VACCINED is NULL;"
            appointment_check = Common().db(appointment_check_query, "fetch")
            self.hide()

            if len(appointment_check) > 0 and self.user["REMIND"] == 1:
                self.reminder_window.settings(appointment_check, self.user)
                self.reminder_window.setModal(True)
                self.reminder_window.exec_()
        except:
            QMessageBox.information(self, "Warning", "Incorrect user name or password.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login_win.btnLogin.click()


app = QApplication([])
login_win = LoginWin()
login_win.show()
app.exec_()
