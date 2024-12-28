import os
import re
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery


class TableSearchDialog(QDialog):
    selected_table_name = pyqtSignal(str)  # Signal to emit the selected table name

    def __init__(self):
        super(TableSearchDialog, self).__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), "views", "tableSearchDialog.ui")
        loadUi(ui_file_path, self)

        # Find UI components
        self.yearDropdown = self.findChild(QComboBox, "yearDropdown")
        self.monthDropdown = self.findChild(QComboBox, "monthDropdown")
        self.viewTableButton = self.findChild(QPushButton, "searchTableViewPushButton")
        self.cancelButton = self.findChild(QPushButton, "searchTableCancelPushButton")

        # Connect signals to slots
        self.yearDropdown.currentIndexChanged.connect(self.on_year_selected)
        self.viewTableButton.clicked.connect(self.on_view_table_clicked)
        self.cancelButton.clicked.connect(self.close)

        # Initialize UI
        self.populate_year_dropdown()

    """
    Populate the year dropdown with unique table years
    """
    def populate_year_dropdown(self):
        years = self.get_unique_table_years()
        self.yearDropdown.clear()
        self.yearDropdown.addItems(years)

    """
    Populate the month dropdown when a year is selected
    """
    def on_year_selected(self):
        selected_year = self.yearDropdown.currentText()
        if selected_year:
            self.populate_month_dropdown(selected_year)

    """
    Populate the month dropdown with months for the selected year
    """
    def populate_month_dropdown(self, selected_year):
        months = self.get_months_for_year(selected_year)
        self.monthDropdown.clear()
        self.monthDropdown.addItems(months)

    """
    Format the selected table name and emit the signal
    """
    def on_view_table_clicked(self):
        selected_year = self.yearDropdown.currentText()
        selected_month = self.monthDropdown.currentText()
        if not selected_year or not selected_month:
            QMessageBox.warning(self, "Selection Error", "Please select both a year and a month.")
            return

        # Format the table name
        table_name = f"{selected_year}_{selected_month}"
        self.selected_table_name.emit(table_name)  # Emit the table name
        self.close()

    """
    Fetch unique years from table names in the database
    
     Returns:
     List[str]: A list of unique years extracted from table names
    """
    def get_unique_table_years(self):
        query = QSqlQuery()
        sql_statement = """
            SELECT DISTINCT SUBSTR(name, 1, 4) AS year
            FROM sqlite_master
            WHERE type = 'table' AND INSTR(name, '_') > 0
            ORDER BY year DESC;
        """
        if not query.exec(sql_statement):
            QMessageBox.critical(self, "Database Error", "Failed to fetch years from the database.")
            return []

        years = []
        while query.next():
            year = query.value(0)
            if re.match(r"^\d{4}$", year):  # Ensure it's a valid 4-digit year
                years.append(year)
        return years

    """
    Fetch unique months for a specific year from table names
    
     Returns:
     List[str]: A list of unique months extracted from table names for the specified year
    """
    def get_months_for_year(self, selected_year):
        query = QSqlQuery()
        sql_statement = f"""
            SELECT DISTINCT SUBSTR(name, INSTR(name, '_') + 1, 2) AS month
            FROM sqlite_master
            WHERE type = 'table' AND name LIKE '{selected_year}_%'
            ORDER BY month ASC;
        """
        if not query.exec(sql_statement):
            QMessageBox.critical(self, "Database Error", "Failed to fetch months from the database.")
            return []

        months = []
        while query.next():
            month = query.value(0)
            if re.match(r"^\d{2}$", month):  # Ensure it's a valid 2-digit month
                months.append(month)
        return months
