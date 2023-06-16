import pymysql
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from datetime import datetime


class Common:
    def __init__(self):
        self.phone_codes_countries = ["Bulgaria (+359)", "Germany (+49)", "India (+91)", "Italy (+39)", "Spain (+34)",
                                      "Turkey (+90)", "United Kingdom (+44)", "United States (+1)"]

    def db(self, query, do):
        database = pymysql.connect(host="localhost",
                                   user="root",
                                   password="Justy1992",
                                   db="vetdb",
                                   charset="utf8mb4",
                                   cursorclass=pymysql.cursors.DictCursor)
        connection = database.cursor()
        connection.execute(query)
        data = connection.fetchall()
        if do == "fetch":
            database.close()
            return data
        elif do == "commit":
            database.commit()
            database.close()

    def date_format(self, date):
        return f"{date[2]}.{date[1]}.{date[0]}"

    def paint_dt(self, chance_this):
        if datetime.today().year - chance_this.date().toPyDate().year < 12:
            chance_this.setStyleSheet("background-color: rgb(213, 213, 213);")
        else:
            chance_this.setStyleSheet("background-color: rgb(255, 255, 255);")

    def phone_codes(self, tool):
        menu = QMenu()
        for phone_code in self.phone_codes_countries:
            action = QAction(phone_code, menu)
            action.triggered.connect(lambda: self.set_phone_code(tool, action))
            menu.addAction(action)
        return menu

    def set_phone_code(self, tool, action):
        tool.setText(action.sender().text().split("(")[1][:-1])

    def address_format(self, ad):
        address = ""
        for i in range(len(ad)):
            if ad[i] != "":
                address += f'{ad[i].replace(", ", "")}, '
        if address[-2:] == ", ":
            address = address[:-2]
        return address

    def user_info(self, u):
        global user
        user = u

    def fetch_user(self):
        return user

    def add(self, win, fetch, cl_id, what):
        try:
            win.add(cl_id)
            win.setModal(True)
            win.exec_()
            fetch()
        except:
            Common().msg(f"Please first select a {what}.")

    def edit(self, tbw, win, what, fetch):
        try:
            query = f"SELECT * FROM {what} WHERE ID ="\
                    f"{tbw.item(tbw.currentRow(), 0).text()};"
            editing = self.db(query, "fetch")[0]
            win.edit(editing)
            win.setModal(True)
            win.exec_()
            fetch()
        except:
            self.msg(f"Please first select the {what.replace('_', ' ')[:-1]} you want to edit.")

    def delete(self, tbw, what, fetch, fetch2):
        try:
            print(tbw.item(tbw.currentRow(), 0).text())
            sure = QMessageBox(QMessageBox.Question, "Attention", f"Are you sure you want to delete this {what.replace('_', ' ')[:-1]}?", QMessageBox.Yes | QMessageBox.No).exec_()
            if sure == QMessageBox.Yes:
                query = f"UPDATE {what} SET DELETED = 1, DATE_OF_DELETE = '{datetime.today()}'" \
                        f" WHERE ID = {tbw.item(tbw.currentRow(), 0).text()}"
                self.db(query, "commit")
                fetch()
                try:
                    fetch2()
                except:
                    pass
        except:
            self.msg(f"Please first select the {what[:-1]} you want to delete.")

    def set_number_of(self, tbw, lbl, what):
        if tbw.rowCount() != 0:
            num = tbw.rowCount()
        else:
            num = ""
        lbl.setText(f"Number of {what.title()}: {num}")

    def msg(self, text):
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon("C:/Users/baris/Desktop/Projects/Vet/Icons/IDEAL_ICON_2.ico"))
        message_box.setIcon(QMessageBox.Critical)
        message_box.setWindowTitle("Warning!")
        message_box.setText(text)
        message_box.exec()

    def save_msg(self):
        sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to save?",
                           QMessageBox.Yes | QMessageBox.No)
        sure.setWindowIcon(QIcon("C:/Users/baris/Desktop/Projects/Vet/Icons/IDEAL_ICON_2.ico"))
        return sure


