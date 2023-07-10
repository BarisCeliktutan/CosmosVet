from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import Reminder_Design
from Common_Codes import Common
from datetime import datetime


class Reminder(QDialog):
    def __init__(self):
        super().__init__()
        self.reminder_win = Reminder_Design.Ui_winApporachingAppointments()
        self.reminder_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.reminder_win.btnYes.clicked.connect(self.set_reminder)
        self.reminder_win.btnNo.clicked.connect(self.set_reminder)

    def settings(self, appointments, user):
        self.user = user
        self.reminder_win.lblMsg.setText(f"You have {appointments} approaching appointments.\nDo you want to see them?")

    def set_reminder(self):
        if self.sender().text() == "YES":
            print("pressed yes")

        query = f"UPDATE users SET REMIND = {not self.reminder_win.cbRemind.isChecked()} WHERE ID = {self.user['ID']}"
        Common().db(query, "commit")
        self.hide()
