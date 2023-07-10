from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from Designs import Appointments_Design
from Common_Codes import Common


class Appointments(QWidget):
    def __init__(self):
        super().__init__()
        self.appointments_win = Appointments_Design.Ui_winAppointments()
        self.appointments_win.setupUi(self)

        self.appointments_win.tbwAppointments.setColumnHidden(0, True)
        self.appointments_win.tbwAppointments.setColumnWidth(1, 186)
        self.appointments_win.tbwAppointments.setColumnWidth(2, 187)
        self.appointments_win.tbwAppointments.setColumnWidth(3, 170)

    def fill_appointments(self, appointments):
        self.appointments_win.tbwAppointments.setRowCount(len(appointments))
        for row, app in enumerate(appointments):
            self.appointments_win.tbwAppointments.setItem(row, 0, QTableWidgetItem(str(app["ID"])))
            self.appointments_win.tbwAppointments.setItem(row, 1, QTableWidgetItem(f"{app['FIRST_NAME']} {app['LAST_NAME']} - {app['PET_NAME']}"))
            self.appointments_win.tbwAppointments.setItem(row, 2, QTableWidgetItem(app["VACCINE_NAME"]))
            try:
                date_of_appointment = Common().date_format(str(app["DATE_OF_APPOINTMENT"]).split("-"))
                self.appointments_win.tbwAppointments.setItem(row, 3, QTableWidgetItem(date_of_appointment))
            except:
                self.appointments_win.tbwAppointments.setItem(row, 3, QTableWidgetItem(""))
