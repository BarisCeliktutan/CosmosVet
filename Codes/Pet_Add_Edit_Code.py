from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtCore
from Designs import Pet_Add_Edit_Design
from Codes import Add_Type_Breed_Code
from Common_Codes import Common
from datetime import datetime


class PetAddEdit(QDialog):
    def __init__(self):
        super().__init__()
        self.pet_add_edit_win = Pet_Add_Edit_Design.Ui_winPetAddEdit()
        self.pet_add_edit_win.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.add_type_window = Add_Type_Breed_Code.AddTypeBreed("pet_types", "TYPE", "Add a New Type")
        self.add_breed_window = Add_Type_Breed_Code.AddTypeBreed("breeds", "BREED", "Add a New Breed")

        self.fill_cbType()
        self.pet_add_edit_win.btnAddPic.clicked.connect(self.add_pic)
        self.pet_add_edit_win.btnSave.clicked.connect(self.save)
        self.pet_add_edit_win.cbType.currentTextChanged.connect(self.cbType_text_changed)
        self.pet_add_edit_win.cbBreed.currentTextChanged.connect(self.cbBreed_text_changed)

    def add(self, cl_id):
        self.cl_id = cl_id[0]
        self.setWindowTitle("Add Pet")
        self.pet_add_edit_win.entChipNo.setText("")
        self.pet_add_edit_win.entName.setText("")
        self.pet_add_edit_win.dtDOB.setDate(datetime.today())
        self.pet_add_edit_win.cbGender.setCurrentText("")
        self.pet_add_edit_win.cbType.setCurrentText("")
        self.pet_add_edit_win.cbBreed.setCurrentText("")
        self.pet_add_edit_win.entColor.setText("")
        self.pet_add_edit_win.entSpecialMark.setText("")
        self.x = "add"
        self.setStyleSheet("background-color: rgb(150, 255, 84);")

    def edit(self, editing):
        self.setWindowTitle(f"Editing {editing['NAME']}")
        self.editing = editing
        self.pet_add_edit_win.entChipNo.setText(editing["CHIP_NO"])
        self.pet_add_edit_win.entName.setText(editing["NAME"])
        self.pet_add_edit_win.dtDOB.setDate(editing["DOB"])
        self.pet_add_edit_win.cbGender.setCurrentText(editing["GENDER"])
        self.pet_add_edit_win.cbType.setCurrentText(editing["TYPE"])
        self.pet_add_edit_win.cbBreed.setCurrentText(editing["BREED"])
        self.pet_add_edit_win.entColor.setText(editing["COLOR"])
        self.pet_add_edit_win.entSpecialMark.setText(editing["SPECIAL_MARK"])
        self.x = "update"
        self.setStyleSheet("background-color: rgb(255, 165, 0);")

    def add_pic(self):
        print("Pressed to ADD PICTURE")

    # def fill_cb(self, cb, what, field): ### Could not entegreted these two functions to eachother
    #     cb.clear()
    #     cb.addItem("")
    #     query = f"SELECT * FROM {what}"
    #     if field == "BREED":
    #         type_id = Common().db(f"SELECT ID FROM pet_types WHERE TYPE = '{self.pet_add_edit_win.cbType.currentText()}'", "fetch")[0]["ID"]
    #         query += f" WHERE TYPE_ID = {type_id}"
    #         self.flag = 1
    #     items = Common().db(query, "fetch")
    #     for i in range(len(items)):
    #         cb.addItem(items[i][field])
    #     cb.addItem(f"+ Add a New {field.title()}")
    #     self.pet_add_edit_win.cbBreed.setCurrentText("")
    #
    # def new_cb_content(self, win, what, field):
    #     if "+ Add a New" in self.sender().currentText():
    #         if self.sender() == self.pet_add_edit_win.cbBreed and self.flag == 1:
    #             self.flag = 0
    #         else:
    #             try:
    #                 type_id = \
    #                 Common().db(f"SELECT ID FROM pet_types WHERE TYPE = '{self.pet_add_edit_win.cbType.currentText()}'",
    #                             "fetch")[0]["ID"]
    #             except:
    #                 type_id = ""
    #             Common().add(win, lambda: self.fill_cb(self.sender(), what, field), type_id, what)
    #     elif self.sender() == self.pet_add_edit_win.cbType and self.sender().currentText() != "":
    #         self.fill_cb(self.pet_add_edit_win.cbBreed, "breeds", "BREED")
    #     else:
    #         self.pet_add_edit_win.cbBreed.clear()

    def fill_cbType(self):
        self.pet_add_edit_win.cbType.clear()
        self.pet_add_edit_win.cbType.addItem("")
        types = Common().db("SELECT TYPE FROM pet_types", "fetch")
        for i in range(len(types)):
            self.pet_add_edit_win.cbType.addItem(types[i]["TYPE"])
        self.pet_add_edit_win.cbType.addItem("+ Add a New Type")
        self.pet_add_edit_win.cbType.setCurrentText("")

    def fill_cbBreed(self):
        self.pet_add_edit_win.cbBreed.clear()
        self.pet_add_edit_win.cbBreed.addItem("")
        try:
            self.type_id = Common().db(f"SELECT ID FROM pet_types WHERE TYPE = '{self.pet_add_edit_win.cbType.currentText()}'", "fetch")[0]["ID"]
            breeds = Common().db(f"SELECT BREED FROM breeds WHERE TYPE_ID = {self.type_id}", "fetch")
            for i in range(len(breeds)):
                self.pet_add_edit_win.cbBreed.addItem(breeds[i]["BREED"])
            self.pet_add_edit_win.cbBreed.addItem("+ Add a New Breed")
            self.pet_add_edit_win.cbBreed.setCurrentText("")
        except:
            self.pet_add_edit_win.cbBreed.clear()

    # def fill_cb(self, cb, field, table):  ###  does not work for filling cbBreed for some reason
    #     cb.clear()
    #     cb.addItem("")
    #     try:
    #         self.type_id = Common().db("SELECT ID FROM pet_types WHERE TYPE = '{self.pet_add_edit_win.cbType.currentText()}'", "fetch")[0]["ID"]
    #         breed_query = f" WHERE TYPE ID = {self.type_id}"
    #     except:
    #         breed_query = ""
    #         self.pet_add_edit_win.cbBreed.clear()
    #     items = Common().db(f"SELECT {field} FROM {table}{breed_query}", "fetch")
    #     for i in range(len(items)):
    #         cb.addItem(items[i][field])
    #     cb.addItem(f"+ Add a New {field.title()}")
    #     cb.setCurrentText("")

    def cbType_text_changed(self):
        if self.sender().currentText() == "+ Add a New Type":
            Common().add(self.add_type_window, self.fill_cbType, self.cl_id, "")
        else:
            self.fill_cbBreed()

    def cbBreed_text_changed(self):
        if self.sender().currentText() == "+ Add a New Breed":
            Common().add(self.add_breed_window, self.fill_cbBreed, self.type_id, "pet type")

    def save(self):
        date_of_entry = datetime.today().date()
        chip_no = self.pet_add_edit_win.entChipNo.text()
        name = self.pet_add_edit_win.entName.text()
        dob = self.pet_add_edit_win.dtDOB.date().toPyDate()
        gender = self.pet_add_edit_win.cbGender.currentText()
        type = self.pet_add_edit_win.cbType.currentText()
        breed = self.pet_add_edit_win.cbBreed.currentText()
        color = self.pet_add_edit_win.entColor.text()
        special_mark = self.pet_add_edit_win.entSpecialMark.toPlainText()

        # clinic_id # db only (fetch bosses clinic id)

        # sure = QMessageBox(QMessageBox.Question, "Attention", "Are you sure you want to save?",
        #                    QMessageBox.Yes | QMessageBox.No).exec_()
        sure = Common().save_msg().exec_()
        if sure == QMessageBox.Yes:
            if self.x == "add":
                query = f"INSERT INTO pets (DATE_OF_ENTRY, CHIP_NO, NAME, DOB, GENDER, TYPE, BREED, COLOR, " \
                        f"SPECIAL_MARK, CLIENT_ID) VALUES ('{date_of_entry}', '{chip_no}', '{name}', '{dob}', " \
                        f"'{gender}', '{type}', '{breed}', '{color}', '{special_mark}', " \
                        f"{self.cl_id})"
            else:
                query = f"UPDATE pets SET DATE_OF_ENTRY = '{date_of_entry}', CHIP_NO = '{chip_no}', " \
                        f"NAME = '{name}', DOB = '{dob}', GENDER = '{gender}', TYPE = '{type}', BREED = " \
                        f"'{breed}', COLOR = '{color}', SPECIAL_MARK = '{special_mark}' WHERE ID = {self.editing['ID']}"

            Common().db(query, 'commit')
            self.hide()
