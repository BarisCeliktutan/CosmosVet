from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5 import QtCore
from Designs import Charges_Design
from Codes import Payment_Code
from Common_Codes import Common


class Charges(QDialog):
    def __init__(self):
        super().__init__()
        self.charges_win = Charges_Design.Ui_winCharges()
        self.charges_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.payment_window = Payment_Code.Payment()

        self.charges_win.btnPaymentAdd.clicked.connect(lambda: Common().add(self.payment_window, self.fetch_charges, self.client_id, "view_charges"))
        self.charges_win.btnPaymentEdit.clicked.connect(lambda: Common().edit(self.charges_win.tbwCharges, self.payment_window, "view_charges", self.fetch_charges))

    def settings(self, client_id, client):
        self.client_id = client_id
        self.fetch_charges()
        self.charges_win.lblClientInfo.setText(f"Charges For {client}")
        self.setWindowTitle(f"Charges For {client}")

    def fetch_charges(self):
        query = f"SELECT * FROM view_charges WHERE CLIENT_ID = {self.client_id} ORDER BY DATE_OF_PAYMENT;"
        self.charges = Common().db(query, "fetch")
        self.fill_charges(self.charges)

    def fill_charges(self, charges):
        self.charges_win.tbwCharges.setRowCount(len(charges))
        paid = 0.00
        if len(charges) > 0:
            for row, charge in enumerate(charges):
                self.charges_win.tbwCharges.setItem(row, 0, QTableWidgetItem(str(charge["ID"])))
                try:
                    date_of_appointment = Common().date_format(str(charge["DATE_OF_PAYMENT"]).split("-"))
                    self.charges_win.tbwCharges.setItem(row, 1, QTableWidgetItem(date_of_appointment))
                except:
                    self.charges_win.tbwCharges.setItem(row, 1, QTableWidgetItem(""))
                self.charges_win.tbwCharges.setItem(row, 2, QTableWidgetItem(charge["PAYMENT_DESCRIPTION"]))
                self.charges_win.tbwCharges.setItem(row, 3, QTableWidgetItem(str(charge["PRICE"])))
                self.charges_win.tbwCharges.setItem(row, 4, QTableWidgetItem(str(charge["CHARGES_PAID"])))
                paid += float(charge["CHARGES_PAID"])
        try:
            self.charges_win.entTotal.setText(f" £ {charges[0]['CHARGES_TOTAL']}")
            self.charges_win.entPaid.setText(f" £ {'%.2f' % paid}")
            self.charges_win.entLeft.setText(f" £ {charges[0]['CHARGES_LEFT']}")
        except:
            self.charges_win.entTotal.setText(f" £ 0.00")
            self.charges_win.entPaid.setText(f" £ 0.00")
            self.charges_win.entLeft.setText(f" £ 0.00")

