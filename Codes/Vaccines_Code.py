from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton, QTableWidgetItem
from PyQt5 import QtCore, QtGui
from Designs import Vaccines_Design
from Codes import New_Vaccine_Code
from Common_Codes import Common
from datetime import datetime


class Vaccines(QDialog):
    def __init__(self):
        super().__init__()
        self.vac_win = Vaccines_Design.Ui_winVaccines()
        self.vac_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.new_vac_window = New_Vaccine_Code.NewVaccine()

        self.vac_win.tbwVaccines.doubleClicked.connect(self.include)

        self.vac_win.btnVaccineAdd.clicked.connect(lambda: Common().add(self.new_vac_window, self.fill_vac, self.pet_id, "vaccines"))
        self.vac_win.btnVaccineEdit.clicked.connect(lambda: Common().edit(self.vac_win.tbwVaccines, self.new_vac_window, "vaccine_types", self.fill_vac))
        self.vac_win.btnVaccineDelete.clicked.connect(lambda: Common().delete(self.vac_win.tbwVaccines, "vaccine_types", self.fill_vac, ""))

    def add(self, ids):
        self.pet_id = ids[0]
        self.cl_id = ids[1]
        self.fill_vac()

    def include(self):
        vac_name = self.vac_win.tbwVaccines.item(self.vac_win.tbwVaccines.currentRow(), 1).text()
        check_query = f"SELECT * FROM vaccines WHERE VACCINE_NAME = '{vac_name}' AND DELETED = 0"
        check = Common().db(check_query, "fetch")
        if len(check) > 1:
            Common().msg("This vaccination is already added!")
        else:
            include_vac_query = f"INSERT INTO vaccines (VACCINE_NAME, DATE_OF_APPOINTMENT, PET_ID) VALUES " \
                                f"('{vac_name}', '{datetime.today()}', {self.pet_id})"
            Common().db(include_vac_query, "commit")
            self.close()

    def fill_vac(self):
        vaccines_query = f"SELECT * FROM vaccine_types WHERE DELETED = 0"
        vaccines = Common().db(vaccines_query, "fetch")
        self.vac_win.tbwVaccines.setRowCount(len(vaccines))
        for row, vac in enumerate(vaccines):
            self.vac_win.tbwVaccines.setItem(row, 0, QTableWidgetItem(str(vac["ID"])))
            self.vac_win.tbwVaccines.setItem(row, 1, QTableWidgetItem(vac["VACCINE_NAME"]))
            self.vac_win.tbwVaccines.setItem(row, 2, QTableWidgetItem(vac["SERIAL_NUMBER"]))
            expiry_date = Common().date_format(str(vac["EXPIRY_DATE"]).split("-"))
            self.vac_win.tbwVaccines.setItem(row, 3, QTableWidgetItem(expiry_date))
            self.vac_win.tbwVaccines.setItem(row, 4, QTableWidgetItem(str(vac["QUANTITY"])))
            self.vac_win.tbwVaccines.setItem(row, 5, QTableWidgetItem(str(vac["PERIOD"])))



