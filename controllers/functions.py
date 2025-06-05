from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from ui.add_expense_dialog import AddExpenseDialog
from ui.add_income_dialog import AddIncomeDialog
from ui.edit_entry_dialog import EditEntryDialog
from ui.table_search_dialog import TableSearchDialog
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

    def open_edit_dialog(self):
        selected_row = self.main_window.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(None, "No Entry Selected", "Please select an entry to edit.")
            return

        entry_data = {
            "id": int(self.main_window.table.item(selected_row, 0).text()),
            "date": self.main_window.table.item(selected_row, 1).text(),
            "store": self.main_window.table.item(selected_row, 2).text(),
            "entry_type": self.main_window.table.item(selected_row, 3).text(),
            "category": self.main_window.table.item(selected_row, 4).text(),
            "amount": float(self.main_window.table.item(selected_row, 5).text().replace("$", "").strip()),
            "description": self.main_window.table.item(selected_row, 6).text(),
        }

        dialog = EditEntryDialog(entry_data, on_update_callback=self.db.update_entry)
        dialog.exec_()

    def handle_add_expense_submit(self, data):
        if self.db.check_duplicate_entry(data):
            response = QMessageBox.question(
                None,
                "Duplicate Entry",
                "An identical expense already exists. Do you want to add it anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.No:
                self.dialog.reject()
                return

        self.db.insert_expense(data)
        self.db.load_table()


    def handle_add_income_submit(self, data):
        if self.db.check_duplicate_entry(data):
            response = QMessageBox.question(
                None,
                "Duplicate Entry",
                "An identical income entry already exists. Do you want to add it anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.No:
                self.dialog.reject()
                return

        self.db.insert_income(data)
        self.db.load_table()

    def duplicate_selected_entry(self):
        selected_row = self.main_window.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(None, "No Entry Selected", "Please select an entry to duplicate.")
            return

        # Extract data from selected row
        data = {
            "date": self.main_window.table.item(selected_row, 1).text(),
            "store": self.main_window.table.item(selected_row, 2).text(),
            "entry_type": self.main_window.table.item(selected_row, 3).text(),
            "category": self.main_window.table.item(selected_row, 4).text(),
            "amount": float(self.main_window.table.item(selected_row, 5).text().replace("$", "").strip()),
            "description": self.main_window.table.item(selected_row, 6).text(),
        }

        # Confirm duplication
        confirm = QMessageBox.question(
            None,
            "Duplicate Entry",
            "You're about to create a duplicate entry. Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        # Ask if user wants to update the date to today
        update_date = QMessageBox.question(
            None,
            "Update Date",
            "Would you like to update the date of the duplicated entry to today?",
            QMessageBox.Yes | QMessageBox.No
        )

        if update_date == QMessageBox.Yes:
            data["date"] = datetime.now().strftime("%Y-%m-%d")

        # Insert the duplicated entry
        if data["entry_type"] == "income":
            self.db.insert_income(data)
        else:
            self.db.insert_expense(data)

        self.db.load_table()

    def open_table_search_dialog(self):
        dialog = TableSearchDialog(self.db)
        if dialog.exec_():
            selected_table = dialog.get_selected_table()
            if selected_table:
                self.db.load_table(table_name=selected_table)