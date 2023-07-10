from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5 import QtCore
from Designs import Vaccines_Design
from Codes import New_Vaccine_Code
from Common_Codes import Common


class Vaccines(QDialog):
    def __init__(self):
        super().__init__()
        self.vac_win = Vaccines_Design.Ui_winVaccines()
        self.vac_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.new_vac_window = New_Vaccine_Code.NewVaccine()

        self.vac_win.tbwVaccines.setColumnHidden(0, True)  # -17
        self.vac_win.tbwVaccines.setColumnWidth(1, 221)
        self.vac_win.tbwVaccines.setColumnWidth(2, 111)
        self.vac_win.tbwVaccines.setColumnWidth(3, 96)
        self.vac_win.tbwVaccines.setColumnWidth(4, 71)
        self.vac_win.tbwVaccines.setColumnWidth(5, 106)


        self.vac_win.btnSelect.clicked.connect(self.select)
        self.vac_win.tbwVaccines.doubleClicked.connect(self.select)

        self.vac_win.btnVaccineAdd.clicked.connect(lambda: Common().add(self.new_vac_window, self.fill_vac, self.cl_id, "vaccine_types"))
        self.vac_win.btnVaccineEdit.clicked.connect(lambda: Common().edit(self.vac_win.tbwVaccines, self.new_vac_window, "vaccine_types", self.fill_vac))
        self.vac_win.btnVaccineDelete.clicked.connect(lambda: Common().delete(self.vac_win.tbwVaccines, "vaccine_types", self.fill_vac, ""))

    def settings(self, cl_id):
        self.flag = False
        self.cl_id = cl_id
        self.fill_vac()

    def select(self):
        self.flag = True
        self.hide()

    def fill_vaccine_name(self):
        return self.vac_win.tbwVaccines.item(self.vac_win.tbwVaccines.currentRow(), 0).text(),\
               self.vac_win.tbwVaccines.item(self.vac_win.tbwVaccines.currentRow(), 1).text(), self.flag

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
