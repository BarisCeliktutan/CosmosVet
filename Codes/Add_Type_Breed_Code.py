from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore
from Designs import Add_Type_Breed_Design
from Common_Codes import Common


class AddTypeBreed(QDialog):
    def __init__(self, what, field, title):
        super().__init__()
        self.add_win = Add_Type_Breed_Design.Ui_winAddTypeBreed()
        self.add_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(title)
        self.add_win.label.setText(f'{field.title()}:')

        self.what = what
        self.field = field
        self.add_win.btnSave.clicked.connect(self.save)

    def add(self, type_id):
        self.type_id = type_id
        self.add_win.entry.setText("")
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def save(self):
        ent = self.add_win.entry.text()
        if ent == "":
            Common().msg(f"Please first enter a {self.field.lower()}.")
        else:
            sure = Common().save_msg().exec_()
            if sure == QMessageBox.Yes:
                if self.field == "TYPE":
                    add_query = f"INSERT INTO {self.what} ({self.field}) VALUES ('{ent}')"
                else:
                    add_query = f"INSERT INTO {self.what} ({self.field}, TYPE_ID) VALUES ('{ent}', {self.type_id})"
                Common().db(add_query, "commit")
                self.close()
