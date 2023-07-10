from PyQt5.QtWidgets import QDialog, QMessageBox, QAction, QMenu, QToolButton
from PyQt5 import QtCore, QtGui
from Designs import Payment_Design
from Common_Codes import Common
from datetime import datetime


class Payment(QDialog):
    def __init__(self):
        super().__init__()
        self.payment_win = Payment_Design.Ui_winPayment()
        self.payment_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.payment_win.btnSave.clicked.connect(self.save)

    def add(self, cl_id):
        self.cl_id = cl_id
        self.payment_win.dtDate.setDate(datetime.today())
        self.payment_win.entDescription.setText("")
        self.payment_win.spinPrice.setValue(0.00)
        self.payment_win.spinPaid.setValue(0.00)

        self.x = "add"
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def edit(self, editing):
        self.cl_id = editing["CLIENT_ID"]
        try:
            self.payment_win.dtDate.setDate(editing["DATE_OF_PAYMENT"])
        except:
            self.payment_win.dtDate.setDate(datetime.today())
        self.payment_win.entDescription.setText(editing["PAYMENT_DESCRIPTION"])
        self.payment_win.spinPrice.setValue(float(editing["PRICE"]))
        self.payment_win.spinPaid.setValue(float(editing["CHARGES_PAID"]))
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def save(self):
        dt = self.payment_win.dtDate.date()
        date_of_payment = dt.toString("yyyy-MM-dd")
        description = self.payment_win.entDescription.toPlainText()
        price = self.payment_win.spinPrice.value()
        paid = self.payment_win.spinPaid.value()

        check_query = f"SELECT SUM(CHARGES_PAID) AS CHARGES_PAID, CHARGES_TOTAL from view_charges WHERE CLIENT_ID = {self.cl_id};"
        check = Common().db(check_query, "fetch")[0]
        if float(check["CHARGES_PAID"]) + paid > float(check["CHARGES_TOTAL"]) + price:
            Common().msg("You cannot take more payment than total charges")
            return

        # clinic_id # db only (fetch bosses clinic id)

        sure = Common().save_msg().exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                paid_query = f"INSERT INTO charges (DATE_OF_PAYMENT, PAYMENT_DESCRIPTION, PRICE, CHARGES_PAID, CLIENT_ID) VALUES ('{date_of_payment}', '{description}', {price}, {paid}, {self.cl_id});"
                Common().db(paid_query, 'commit')
                left_query = f"UPDATE clients SET CHARGES_LEFT = CHARGES_LEFT + {price} - {paid}, CHARGES_TOTAL = (SELECT sum(PRICE) from charges where CLIENT_ID = {self.cl_id}) WHERE ID = {self.cl_id};"
                Common().db(left_query, 'commit')
            else:
                left_query = f"UPDATE clients SET CHARGES_LEFT = CHARGES_LEFT - {paid} + (SELECT CHARGES_PAID FROM charges WHERE CLIENT_ID = {self.cl_id}) WHERE ID = {self.cl_id};"
                Common().db(left_query, 'commit')
                paid_query = f"UPDATE charges SET CHARGES_PAID = {paid}, DATE_OF_PAYMENT = '{date_of_payment}', PRICE = {price}, PAYMENT_DESCRIPTION = '{description}' WHERE CLIENT_ID = {self.cl_id};"
                Common().db(paid_query, 'commit')


            self.hide()
