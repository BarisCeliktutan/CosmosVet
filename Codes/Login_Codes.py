from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from Designs import Login_Design
from Codes import Main_Win_Code
from Common_Codes import Common
from getmac import get_mac_address


class LoginWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_win = Login_Design.Ui_winLogin()
        self.login_win.setupUi(self)
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;", "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)
        self.flag = 0

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
            query = f"UPDATE users SET REMEMBER_ME = {self.login_win.cbRememberMe.isChecked()}{mac_code}, " \
                    f"LAST_LOGIN = 1 WHERE ID = '{self.user['ID']}'"
            Common().db(query, "commit")

            last_login_query = f"UPDATE users SET LAST_LOGIN = 0 WHERE MAC LIKE '%{self.mac}%' AND USER_NAME <> '{user_name}';"
            Common().db(last_login_query, "commit")
            Common().user_info(self.user)
            self.main_window.settings()
            self.main_window.show()
            self.hide()
        except:
            QMessageBox.information(self, "Warning", "Incorrect user name or password.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login_win.btnLogin.click()


app = QApplication([])
login_win = LoginWin()
login_win.show()
app.exec_()
