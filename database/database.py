import sys
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime

class Database:
    def __init__(self, main_window):
        super().__init__()

        # Create and open database
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

    def create_table(self, current_month):
        """Create table with updated schema."""
        query = QSqlQuery()
        query.exec_(f"""
            CREATE TABLE IF NOT EXISTS "{current_month}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                source TEXT,
                entry_type TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
        """)

    def load_table(self):
        """Loads the entries from the current monthly table into the UI table."""
        self.main_window.table.setRowCount(0)

        query = QSqlQuery(f"""SELECT * FROM "{self.current_table}" """)
        row = 0
        while query.next():
            entry_id = query.value(0)
            date = query.value(1)
            source = query.value(2)
            entry_type = query.value(3)
            category = query.value(4)
            amount = query.value(5)
            description = query.value(6)

            self.main_window.table.insertRow(row)
            self.main_window.table.setItem(row, 0, QTableWidgetItem(str(entry_id)))
            self.main_window.table.setItem(row, 1, QTableWidgetItem(date))
            self.main_window.table.setItem(row, 2, QTableWidgetItem(source))
            self.main_window.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.main_window.table.setItem(row, 4, QTableWidgetItem(category))
            self.main_window.table.setItem(row, 5, QTableWidgetItem(f"{amount:.2f}"))
            self.main_window.table.setItem(row, 6, QTableWidgetItem(description))

            row += 1

    def insert_expense(self, data):
        self._insert_entry(data)

    def insert_income(self, data):
        self._insert_entry(data)

    def _insert_entry(self, data):
        """Shared method for inserting expense or income."""
        query = QSqlQuery()
        query.prepare(f"""
            INSERT INTO "{self.current_table}" (date, source, entry_type, category, amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(data["date"])
        query.addBindValue(data["store"])
        query.addBindValue(data["entry_type"])
        query.addBindValue(data["category"])
        query.addBindValue(data["amount"])
        query.addBindValue(data["description"])

        if not query.exec_():
            QMessageBox.critical(None, "Database Error", f"Failed to add entry:\n{query.lastError().text()}")

    def add_expense(self, date, source, category, amount, description):
        self._insert_entry({
            "date": date,
            "store": source,
            "entry_type": "expense",
            "category": category,
            "amount": amount,
            "description": description
        })

    def add_income(self, date, source, category, amount, description):
        self._insert_entry({
            "date": date,
            "store": source,
            "entry_type": "income",
            "category": category,
            "amount": amount,
            "description": description
        })

    def delete_entry(self):
        """Deletes selected entry (expense or income)."""
        selected_row = self.main_window.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to delete!")
            return

        entry_id = int(self.main_window.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(None, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare(f"""DELETE FROM "{self.current_table}" WHERE id = ?""")
        query.addBindValue(entry_id)
        query.exec_()
        self.load_table()
