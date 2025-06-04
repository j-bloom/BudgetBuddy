import datetime
import csv
from difflib import SequenceMatcher
import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog, QAbstractItemView, QTextEdit, QVBoxLayout, QLabel, QInputDialog, QLineEdit
from PyQt5.QtGui import QFont
import controllers.ocr
from database import Database
from editEntry import EditDialog
from expenses import ExpenseDialog
from income import IncomeDialog
from PyQt5.QtSql import QSqlQuery
from fpdf import FPDF
import pytesseract
from PIL import Image
import controllers.functions
from controllers.csv import export_to_csv, import_from_csv
import controllers.ocr
from controllers.pdf import export_to_pdf
from tableSearch import TableSearchDialog

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), "views", "welcomescreen.ui")
        loadUi(ui_file_path, self)

        self.current_table = None
        
        """
        Create the database table with the name of the current year and month,
        allowing the monthly overview to be displayed
        """
        self.db = Database()
        month = controllers.functions.get_current_year_month()
        self.current_table = month
        self.db.create_table(self.current_table)

        """
        Setup the table object to modify the header
        Stretch the header to fit the full width of the table
        """
        self.table = self.findChild(QTableWidget, "MonthlyTableOverview")

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.handle_double_click)


        """
        Connect the income/expense buttons to their respective views/dialogs
        """
        self.addExpenseBtn.clicked.connect(self.display_expense_dialog)
        self.addIncomeBtn.clicked.connect(self.display_income_dialog)
        self.monthlyViewBtn.clicked.connect(self.display_table_search_dialog)

        """
        Connect the import/export buttons for additional feature functionality
        """
        self.csvExportBtn.clicked.connect(self.export_to_csv)
        self.csvImportBtn.clicked.connect(self.import_from_csv)
        self.pdfExportBtn.clicked.connect(self.export_to_pdf)
        self.screenshotImportBtn.clicked.connect(self.import_screenshot_image)
        self.searchFilterInput.textChanged.connect(self.filter_table)
        
        self.editEntryBtn.clicked.connect(self.edit_entry)
        self.deleteEntryBtn.clicked.connect(self.delete_entry)
        self.duplicateEntryBtn.clicked.connect(self.duplicate_entry)

        """
        Filter functionality based on the different budgeting fields
        """

        self.active_filters = {
            "source": None,
            "category": None,
            "entry_type": None,
            "min_amount": None,
            "max_amount": None,
            "description": None
        }

        self.sourceSort.addItem("All")
        self.sourceSort.addItems(self.get_unique_sources(self.current_table))

        self.sourceSort.setCurrentText("All")
        self.sourceSort.currentTextChanged.connect(self.filter_by_source)

        self.categorySort.setCurrentText("All")
        self.categorySort.currentTextChanged.connect(self.filter_by_category)

        self.entryTypeSort.setCurrentText("All")
        self.entryTypeSort.currentTextChanged.connect(self.filter_by_entry_type)

        self.min_spinbox.valueChanged.connect(self.apply_numeric_filter)
        self.max_spinbox.valueChanged.connect(self.apply_numeric_filter)

        self.descriptionSort.textChanged.connect(self.filter_by_description)

        self.clearFilterTableBtn.clicked.connect(self.clear_filters)
      
        self.update_totals(self.current_table)
        self.load_table(self.current_table)
        
    def handle_double_click(self, row, column):
        if column == 5:  # Check if the "Description" column is clicked
            description = self.table.item(row, column).text()
            self.show_description_popup(description)
    
    def show_description_popup(self, description):
        dialog = QDialog(self)
        dialog.setWindowTitle("Full Description")
        dialog.resize(400, 200)
        
        layout = QVBoxLayout()
        label = QLabel("Full Description:")
        label_font = QFont()
        label_font.setPointSize(12)
        label.setFont(label_font)
        layout.addWidget(label)
        
        # Read-only text edit
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(description)
        text_edit_font = QFont()
        text_edit_font.setPointSize(12)
        text_edit.setFont(text_edit_font)
        layout.addWidget(text_edit)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def duplicate_entry(self):
        """
        Duplicates the selected entry, appends ' - (Copy)' to the description,
        and inserts it into the database and QTableWidget using a prepared statement.
        """
        # Check if a row is selected
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an entry to duplicate.")
            return

        # Get the selected row index
        selected_row = self.table.currentRow()

        # Extract data from the selected row
        date = self.table.item(selected_row, 0).text()
        source = self.table.item(selected_row, 1).text()
        category = self.table.item(selected_row, 2).text()
        entry_type = self.table.item(selected_row, 3).text()
        amount = self.table.item(selected_row, 4).text()
        description = self.table.item(selected_row, 5).text()

        # Append " - (Copy)" to the description
        new_description = f"{description} - (Copy)"

        # Prepare the SQL query for insertion
        query = QSqlQuery()
        query.prepare(f"""
            INSERT INTO '{self.current_table}' (date, source, category, entry_type, amount, description)
            VALUES (:date, :source, :category, :entry_type, :amount, :description)
        """)

        # Bind values to the query
        query.bindValue(":date", date)
        query.bindValue(":source", source)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", new_description)

        # Execute the query
        if query.exec_():
            # Add the duplicated entry to the QTableWidget
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(date))
            self.table.setItem(row_position, 1, QTableWidgetItem(source))
            self.table.setItem(row_position, 2, QTableWidgetItem(category))
            self.table.setItem(row_position, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row_position, 4, QTableWidgetItem(amount))
            self.table.setItem(row_position, 5, QTableWidgetItem(new_description))

            QMessageBox.information(self, "Success", "Entry duplicated successfully!")
        else:
            # Show an error message if the query fails
            error_message = query.lastError().text()
            QMessageBox.critical(self, "Error", f"Failed to duplicate entry: {error_message}")

        self.reload_table()

    """
    Delete selected entry from SQL database based on the entry id
    """
    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to delete!")
            return

        # Get the values of the selected row to identify the entry in the database
        date = self.table.item(selected_row, 0).text()
        source = self.table.item(selected_row, 1).text()
        category = self.table.item(selected_row, 2).text()
        entry_type = self.table.item(selected_row, 3).text()
        amount = self.table.item(selected_row, 4).text()
        description = self.table.item(selected_row, 5).text()

        confirm = QMessageBox.question(self, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)


        if confirm == QMessageBox.No:
            return

        month = controllers.functions.get_current_year_month()
        if self.current_table is None:
            self.current_table = month

        query = QSqlQuery()
        query.prepare(f"""DELETE FROM '{self.current_table}' 
                        WHERE 
                            date = :date AND 
                            source = :source AND
                            category = :category AND 
                            entry_type = :entry_type AND 
                            amount = :amount AND 
                            description = :description
                        """)

        query.bindValue(":date", date)
        query.bindValue(":source", source)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)

        if not query.exec_():
            QMessageBox.warning(self, "Error", "Failed to delete entry: " + query.lastError().text())
        else:
            self.reload_table()  

    def apply_numeric_filter(self):
        min_value = self.min_spinbox.value()
        max_value = self.max_spinbox.value()
        self.filter_by_amount(min_value, max_value)

    def update_totals(self, selected_table):
        expenses = self.db.get_total_amounts(selected_table, "Expense")
        expenses = float(expenses) if expenses else 0.0
        self.totalExpensesAmount.setText(f"$ {expenses:.2f}")
        income = self.db.get_total_amounts(selected_table, "Income")
        income = float(income) if income else 0.0
        self.totalIncomeAmount.setText(f"$ {income:.2f}")
    
    def edit_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to edit!")
            return
        
        month = controllers.functions.get_current_year_month()
        if self.current_table is None:
            self.current_table = month

        date = self.table.item(selected_row, 0).text()
        source = self.table.item(selected_row, 1).text()
        category = self.table.item(selected_row, 2).text()
        entry_type = self.table.item(selected_row, 3).text()
        amount = self.table.item(selected_row, 4).text()
        description = self.table.item(selected_row, 5).text()

        # Pass the data and record ID to the EditDialog
        edit_dialog = EditDialog(self, current_table={self.current_table}, date=date, source=source, category=category, entry_type=entry_type, amount=amount, description=description)
        edit_dialog.entry_updated.connect(self.reload_table)  # Connect the signal
        edit_dialog.exec_()

    def display_expense_dialog(self):
        expense_dialog = ExpenseDialog(self.current_table)
        expense_dialog.entry_added.connect(self.reload_table)
        expense_dialog.exec_()

    def display_income_dialog(self):
        income_dialog = IncomeDialog(self.current_table)
        income_dialog.entry_added.connect(self.reload_table)
        income_dialog.exec_()

    def display_table_search_dialog(self):
        table_search_dialog = TableSearchDialog()
        table_search_dialog.selected_table_name.connect(self.load_table)
        table_search_dialog.selected_table_name.connect(self.update_totals)
        self.current_table = table_search_dialog.selected_table_name
        table_search_dialog.exec_()

    """
    Populate the monthly overview table with the data from the database

    Returns:
    All entries from the specified table in the database
    """
    def load_table(self, table_name=None):
        self.table.setRowCount(0)
        self.current_table = table_name
        query = QSqlQuery(f"SELECT * FROM '{self.current_table}' ORDER BY date DESC")
        row = 0
        while query.next():
            date = query.value(1)
            source = query.value(2)
            category = query.value(3)
            entry_type = query.value(4)
            amount = query.value(5)
            description = query.value(6)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(source))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 5, QTableWidgetItem(description))

            row += 1

    def reload_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.update_totals(self.current_table)
        self.load_table(self.current_table)
        self.sourceSort.clear()
        self.sourceSort.addItem("All")
        self.sourceSort.addItems(self.get_unique_sources(self.current_table))
        self.sourceSort.setCurrentText("All")


    def export_to_csv(self):
        export_to_csv(self.table, self)

    def import_from_csv(self):
        month = controllers.functions.get_current_year_month()

        if self.current_table is None:
            self.current_table = month
            
        import_from_csv(self.table, self, self.current_table)
        self.reload_table()

    def filter_table(self):
        search_text = self.searchFilterInput.text().strip().lower()
        
        if not search_text:
            # If search box is cleared, show all rows
            for row in range(self.table.rowCount()):
                self.table.setRowHidden(row, False)
            return
        
        for row in range(self.table.rowCount()):
            row_match = False
            for col in range(self.table.columnCount()):
                cell_text = self.table.item(row, col).text().lower() if self.table.item(row, col) else ""
                
                similarity = SequenceMatcher(None, search_text, cell_text).ratio()
                
                if search_text in cell_text or similarity > 0.7:
                    row_match = True
                    break
            
            self.table.setRowHidden(row, not row_match)

    def export_to_pdf(self):
        export_to_pdf(self, self.table)

    def import_screenshot_image(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if needed
        # Open a file dialog to select the image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.PNG *.jpg *.jpeg *.bmp)")
        
        month = controllers.functions.get_current_year_month()
        if self.current_table is None:
            self.current_table = month
        
        if file_path:

            current_month = self.current_table  # Get the current month/year for the table name
            controllers.ocr.process_ocr_and_insert(file_path, current_month)
            self.reload_table()  # Reload the table after inserting

    """
    Get unique sources for the selected month and populate the source dropdown menu
    """
    def get_unique_sources(self, month):
        sources = []
        query = QSqlQuery()
        query.exec_(f"SELECT DISTINCT source FROM '{self.current_table}'")
        while query.next():
            sources.append(query.value(0))
        return sources
    
    def filter_by_source(self, selected_source):
        self.active_filters["source"] = None if selected_source == "All" else selected_source
        self.apply_all_filters()

    def filter_by_category(self, selected_category):
        self.active_filters["category"] = None if selected_category == "All" else selected_category
        self.apply_all_filters()

    def filter_by_entry_type(self, selected_entry_type):
        self.active_filters["entry_type"] = None if selected_entry_type == "All" else selected_entry_type
        self.apply_all_filters()

    def filter_by_amount(self, min_value, max_value):
        self.active_filters["min_amount"] = min_value
        self.active_filters["max_amount"] = max_value
        self.apply_all_filters()

    def filter_by_description(self):
        filter_text = self.descriptionSort.text().strip().lower()
        self.active_filters["description"] = None if not filter_text else filter_text
        self.apply_all_filters()

    def apply_all_filters(self):
        for row in range(self.table.rowCount()):
            show_row = True

            # Check source filter
            source_item = self.table.item(row, 1)  # Source column index
            if self.active_filters["source"] and (not source_item or source_item.text().lower() != self.active_filters["source"].lower()):
                show_row = False

            # Check category filter
            category_item = self.table.item(row, 2)  # Category column index
            if self.active_filters["category"] and (not category_item or category_item.text().lower() != self.active_filters["category"].lower()):
                show_row = False

            # Check entry type filter
            entry_type_item = self.table.item(row, 3)  # Entry Type column index
            if self.active_filters["entry_type"] and (not entry_type_item or entry_type_item.text().lower() != self.active_filters["entry_type"].lower()):
                show_row = False

            # Check amount filter
            amount_item = self.table.item(row, 4)  # Amount column index
            if amount_item:
                try:
                    amount_value = float(amount_item.text())
                    if self.active_filters["min_amount"] and amount_value < self.active_filters["min_amount"]:
                        show_row = False
                    if self.active_filters["max_amount"] and amount_value > self.active_filters["max_amount"]:
                        show_row = False
                except ValueError:
                    show_row = False
            elif self.active_filters["min_amount"] or self.active_filters["max_amount"]:
                show_row = False

            # Check description filter
            description_item = self.table.item(row, 5)  # Description column index
            if self.active_filters["description"]:
                description_text = description_item.text().strip().lower() if description_item else ""
                if self.active_filters["description"] not in description_text:
                    show_row = False

            # Show or hide row based on all filters
            self.table.setRowHidden(row, not show_row)

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