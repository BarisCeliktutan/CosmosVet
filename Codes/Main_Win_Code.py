from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QTableWidgetItem
from PyQt5 import QtGui
from Designs import Main_Win_Design
from Codes import Users_Codes, Par_Of_Educ_Codes, Clients_And_Pets_Info_Code
from Common_Codes import Common


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win = Main_Win_Design.Ui_winMain()
        self.main_win.setupUi(self)
        self.user_win_flag = 0
        self.par_of_educ_win_flag = 0
        self.cl_pet_info_win_flag = 0

    def users(self):
        if self.user_win_flag == 0:
            self.users_window.settings()
            self.user_win_flag = 1
        self.users_window.fill_users()
        self.users_window.show()

    def par_of_educ(self):
        if self.par_of_educ_win_flag == 0:
            self.par_of_educ_window.settings()
            self.par_of_educ_win_flag = 1
        self.par_of_educ_window.fetch_clients()
        self.par_of_educ_window.show()

    def cl_pet_info(self):
        if self.cl_pet_info_win_flag == 0:
            self.cl_pet_info_window.settings()
            self.cl_pet_info_win_flag = 1
        self.cl_pet_info_window.fetch_clients()
        self.cl_pet_info_window.showMaximized()

    def settings(self):
        self.user = Common().fetch_user()
        self.users_window = Users_Codes.Users()
        self.par_of_educ_window = Par_Of_Educ_Codes.ParOfEduc()
        self.cl_pet_info_window = Clients_And_Pets_Info_Code.ClientsAndPetsInfo()
        icon = QtGui.QIcon.fromTheme(str(Common().db("SELECT PATH FROM IMAGES WHERE ID = 1;",
                                                     "fetch")[0]["PATH"])[2:-1])
        self.setWindowIcon(icon)

        self.main_win.btnUsers.clicked.connect(self.users)
        self.main_win.btnParOfEduc.clicked.connect(self.par_of_educ)
        self.main_win.btnClPetInfo.clicked.connect(self.cl_pet_info)
        self.setWindowTitle(f"Cosmos Vet - {self.user['FIRST_NAME']} {self.user['LAST_NAME']}")

    def closeEvent(self, event):
        sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to quit?",
                           QMessageBox.Yes | QMessageBox.No).exec_()
        if sure == QMessageBox.No:
            event.ignore()
        else:
            exit()

# from turtle import *
#
# color('red')
# bgcolor('black')
# speed(144)
# hideturtle()
# b = 0
# while b < 200:
#     right(b)
#     forward(b*3)
#     b += 1
#     if b == 199:
#         b = 0
#

