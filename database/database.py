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

    def load_table(self, table_name=None):
        """Loads entries from the current or specified monthly table into the UI table."""
        if table_name:
            self.current_table = table_name

        self.main_window.table.setRowCount(0)

        query = QSqlQuery(f"""SELECT * FROM "{self.current_table}" """)
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            source = query.value(2)
            entry_type = query.value(3)
            category = query.value(4)
            amount = query.value(5)
            description = query.value(6)

            self.main_window.table.insertRow(row)
            self.main_window.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.main_window.table.setItem(row, 1, QTableWidgetItem(date))
            self.main_window.table.setItem(row, 2, QTableWidgetItem(source))
            self.main_window.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.main_window.table.setItem(row, 4, QTableWidgetItem(category))
            self.main_window.table.setItem(row, 5, QTableWidgetItem(f"{amount:.2f}"))
            self.main_window.table.setItem(row, 6, QTableWidgetItem(description))

            row += 1

        self.update_totals()


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

    def update_entry(self, data, check_only=False):
        if check_only:
            # Don't match on the current ID
            query = QSqlQuery()
            query.prepare(f"""
                SELECT COUNT(*) FROM "{self.current_table}"
                WHERE date = ? AND source = ? AND entry_type = ? AND category = ? AND amount = ? AND description = ?
                AND id != ?
            """)
            query.addBindValue(data["date"])
            query.addBindValue(data["store"])
            query.addBindValue(data["entry_type"])
            query.addBindValue(data["category"])
            query.addBindValue(data["amount"])
            query.addBindValue(data["description"])
            query.addBindValue(data["id"])
            if query.exec_() and query.next():
                return query.value(0) > 0
            return False

        # Normal update
        query = QSqlQuery()
        query.prepare(f"""
            UPDATE "{self.current_table}"
            SET date = ?, source = ?, entry_type = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        """)
        query.addBindValue(data["date"])
        query.addBindValue(data["store"])
        query.addBindValue(data["entry_type"])
        query.addBindValue(data["category"])
        query.addBindValue(data["amount"])
        query.addBindValue(data["description"])
        query.addBindValue(data["id"])

        if not query.exec_():
            QMessageBox.critical(None, "Database Error", f"Failed to update entry:\n{query.lastError().text()}")
        else:
            self.load_table()

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

    def check_duplicate_entry(self, data):
        query = QSqlQuery()
        query.prepare(f"""
            SELECT COUNT(*) FROM "{self.current_table}"
            WHERE date = ? AND source = ? AND entry_type = ? AND category = ? AND amount = ? AND description = ?
        """)
        query.addBindValue(data["date"])
        query.addBindValue(data["store"])
        query.addBindValue(data["entry_type"])
        query.addBindValue(data["category"])
        query.addBindValue(data["amount"])
        query.addBindValue(data["description"])

        if query.exec_() and query.next():
            return query.value(0) > 0
        return False

    def update_totals(self):
        """Updates the total income and expense labels on the main window."""
        total_income = 0.0
        total_expense = 0.0

        query = QSqlQuery(f'SELECT entry_type, amount FROM "{self.current_table}"')
        while query.next():
            entry_type = query.value(0)
            amount = query.value(1)

            if entry_type == "income":
                total_income += float(amount)
            elif entry_type == "expense":
                total_expense += float(amount)

        self.main_window.total_income_amount_label.setText(f"${total_income:.2f}")
        self.main_window.total_expense_amount_label.setText(f"${total_expense:.2f}")

    """
    Get unique sources for the selected month and populate the source dropdown menu
    """
    def get_unique_sources(self):
        sources = []
        query = QSqlQuery()
        query.exec_(f"SELECT DISTINCT source FROM '{self.current_table}'")
        while query.next():
            sources.append(query.value(0))
        return sources
    