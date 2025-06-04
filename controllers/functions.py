from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from ui.add_expense_dialog import AddExpenseDialog
from ui.add_income_dialog import AddIncomeDialog
from datetime import datetime

class Functions:
    def __init__(self, main_window, db):
        self.main_window = main_window
        self.db = db
        self.dialog = None

    def open_add_expense_dialog(self):
        self.dialog = AddExpenseDialog(on_submit_callback=self.handle_add_expense_submit)
        self.dialog.setWindowModality(True)
        self.dialog.exec_()

    def open_add_income_dialog(self):
        self.dialog = AddIncomeDialog(on_submit_callback=self.handle_add_income_submit)
        self.dialog.setWindowModality(True)
        self.dialog.exec_()

    def handle_add_expense_submit(self, data):
        self.db.insert_expense(data)
        self.db.load_table()

    def handle_add_income_submit(self, data):
        self.db.insert_income(data)
        self.db.load_table()
