# Imports
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime

class Database():
    def __init__(self, main_window):
        super().__init__()
        
        # Create Database
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("budget.db")

        if not database.open():
            QMessageBox.critical(None, "Error", "Could not open your Database")
            sys.exit(1)

        self.current_table = self.get_monthly_table_name()
        self.create_table(self.current_table)
        self.main_window = main_window


    def get_monthly_table_name(self):
        """Returns the current table name in YYYY_MM format (e.g., 2025_06)."""
        return datetime.now().strftime('%Y_%m')

    def load_table(self):
        self.main_window.table.setRowCount(0)

        query = QSqlQuery(f"""
                          SELECT * FROM "{self.current_table}"
                          """)
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Add values to table
            self.main_window.table.insertRow(row)

            self.main_window.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.main_window.table.setItem(row, 1, QTableWidgetItem(date))
            self.main_window.table.setItem(row, 2, QTableWidgetItem(category))
            self.main_window.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.main_window.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        date = self.main_window.date_box.date().toString("yyyy-MM-dd")
        category = self.main_window.dropdown.currentText()
        amount = self.main_window.amount.text()
        description = self.main_window.description.text()

        query = QSqlQuery()
        query.prepare(f"""
                    INSERT INTO "{self.current_table}" (date, category, amount, description)
                    VALUES (?, ?, ?, ?)
                    """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.main_window.date_box.setDate(QDate.currentDate())
        self.main_window.dropdown.setCurrentIndex(0)
        self.main_window.amount.clear()
        self.main_window.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.main_window.table.currentRow()
        if selected_row == -1:
            confirm = QMessageBox.warning(None, "No Expense Chosen", "Please select an expense to delete!")
            return
        
        expense_id = int(self.main_window.table.item(selected_row, 0).text())

        confirm = QMessageBox.question(None, "Delete Item", "Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare(f"""
                    DELETE FROM "{self.current_table}" WHERE id = ?
                    """)
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()



    def create_table(self, current_month):
        query = QSqlQuery()
        query.exec_(f"""
                    CREATE TABLE IF NOT EXISTS "{current_month}" (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT
                    )
                    """)