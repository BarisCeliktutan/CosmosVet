from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from Designs import Reminder_Design
from Codes import Appointments_Code
from Common_Codes import Common


class Reminder(QDialog):
    def __init__(self):
        super().__init__()
        self.reminder_win = Reminder_Design.Ui_winApporachingAppointments()
        self.reminder_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.appointments_window = Appointments_Code.Appointments()

        self.reminder_win.btnYes.clicked.connect(self.set_reminder)
        self.reminder_win.btnNo.clicked.connect(self.set_reminder)

    def settings(self, appointments, user):
        self.user = user
        self.appointments = appointments
        self.reminder_win.lblMsg.setText(f"You have {len(appointments)} coming appointments.\nDo you want to see them?")

    def set_reminder(self):
        if self.sender().text() == "YES":
            self.appointments_window.fill_appointments(self.appointments)
            self.appointments_window.show()

        query = f"UPDATE users SET REMIND = {not self.reminder_win.cbRemind.isChecked()} WHERE ID = {self.user['ID']}"
        Common().db(query, "commit")
        self.hide()
