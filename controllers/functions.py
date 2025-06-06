from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QFileDialog
from ui.add_expense_dialog import AddExpenseDialog
from ui.add_income_dialog import AddIncomeDialog
from ui.edit_entry_dialog import EditEntryDialog
from ui.table_search_dialog import TableSearchDialog
from datetime import datetime
import pytesseract
from controllers.pdf import export_to_pdf
from controllers.csv import export_to_csv, import_from_csv
import controllers.ocr
from difflib import SequenceMatcher

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

    def handle_export_pdf(self):
        export_to_pdf(self.db.current_table)

    def handle_export_csv(self):
        export_to_csv(self.main_window.table, self.main_window)

    def handle_import_csv(self):
        import_from_csv(self.main_window.table, self.main_window, self.db.current_table)
        self.db.load_table()

    def handle_import_screenshot(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if needed

        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Select Image",
            "",
            "Image Files (*.png *.PNG *.jpg *JPG *.jpeg *JPEG *.bmp)"
        )

        if not file_path:
            return

        # Determine the current month's table name
        current_month = self.db.current_table or datetime.now().strftime("%Y_%m")

        # Run OCR and insert entries
        controllers.ocr.process_ocr_and_insert(file_path, current_month)

        # Refresh the table
        self.db.load_table()

    def clear_filters(self):
        # Reset text-based filters
        self.active_filters = {
            "source": None,
            "category": None,
            "entry_type": None,
            "min_amount": None,
            "max_amount": None,
            "description": None
        }

        self.searchFilterInput.setText("")
        self.descriptionSort.setText("")
        self.sourceSort.setCurrentIndex(0)
        self.categorySort.setCurrentIndex(0)
        self.entryTypeSort.setCurrentIndex(0)

        self.min_spinbox.setValue(0.00)
        self.max_spinbox.setValue(0.00)

        self.apply_all_filters()

        self.reload_table()

    def filter_table(self):
        search_text = self.main_window.filter_search.text().strip().lower()
        
        if not search_text:
            # If search box is cleared, show all rows
            for row in range(self.main_window.table.rowCount()):
                self.main_window.table.setRowHidden(row, False)
            return
        
        for row in range(self.main_window.table.rowCount()):
            row_match = False
            for col in range(self.main_window.table.columnCount()):
                cell_text = self.main_window.table.item(row, col).text().lower() if self.main_window.table.item(row, col) else ""
                
                similarity = SequenceMatcher(None, search_text, cell_text).ratio()
                
                if search_text in cell_text or similarity > 0.7:
                    row_match = True
                    break
            
            self.main_window.table.setRowHidden(row, not row_match)