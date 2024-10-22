"""
Import necessary modules to build the GUI
and run the application
"""
import datetime
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
import os

"""
Main class
"""
class WelcomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join('ui', 'welcomescreen.ui')
        loadUi(ui_path, self)
        self.addExpenseView.clicked.connect(self.navigate_to_expense_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

        month = self.get_current_month_year()
        self.create_table(month)

    def navigate_to_expense_view(self):
        expense = Expense()
        widget.addWidget(expense)
        widget.setCurrentWidget(expense)

    def navigate_to_income_view(self):
        income = Income()
        widget.addWidget(income)
        widget.setCurrentWidget(income)

    """
    Create the table if it doesn't exist
    """
    def create_table(self, month):
        query = QSqlQuery()
        query.exec_(f"""CREATE TABLE IF NOT EXISTS '{month}' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        date DATE,
                        category TEXT,
                        entry_type TEXT DEFAULT 'expense',
                        amount REAL,
                        description TEXT
                    )
                    """)
        

    """
    Get current month and year for table creation formated as "YYYY_MM"
    """
    def get_current_month_year(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year
    
    """
    Load table with entries from SQL database
    """
    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_month_year()
        query = QSqlQuery(f"SELECT * FROM '{month}' ORDER BY date DESC")
        row = 0
        while query.next():
            entry_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            entry_type = query.value(3)
            amount = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(entry_id))) 
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 5, QTableWidgetItem(description))

            row += 1

        """
        Setup table structure for displaying entries
        """
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Entry Type", "Amount", "Description"])


"""
Expense class
"""
class Expense(QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join('ui', 'expensescreen.ui')
        loadUi(ui_path, self)
        self.monthlyView.clicked.connect(self.navigate_to_monthly_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

        self.addExpense.clicked.connect(self.add_entry)
        self.deleteExpense.clicked.connect(self.delete_entry)
        
        self.table = self.findChild(QTableWidget, "tableWidget")  # Update this with the actual name from the .ui file

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Entry Type", "Amount", "Description"])

        self.load_table()

    def navigate_to_monthly_view(self):
        monthly_view = WelcomeScreen()
        widget.addWidget(monthly_view)
        widget.setCurrentWidget(monthly_view)

    def navigate_to_income_view(self):
        income = Income()
        widget.addWidget(income)
        widget.setCurrentWidget(income)

    """
    Get current month and year for table creation formated as "YYYY_MM"
    """
    def get_current_month_year(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year

    """
    Load table with entries from SQL database
    """
    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_month_year()
        query = QSqlQuery(f"SELECT * FROM '{month}' WHERE entry_type == 'expense' ORDER BY date DESC")
        row = 0
        while query.next():
            entry_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            entry_type = query.value(3)
            amount = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(entry_id))) 
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 5, QTableWidgetItem(description))

            row += 1

    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        entry_type = "expense"
        amount = self.amount.text()
        description = self.description.toPlainText()

        month = self.get_current_month_year()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, category, entry_type, amount, description) 
                            VALUES (:date, :category, :entry_type, :amount, :description)
                        """)
        
        query.bindValue(":date", date)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(self, "Add Entry Failed", f"Failed to add entry: {error}")
        else:
            self.date_box.setDate(QDate.currentDate())
            self.dropdown.setCurrentIndex(0)
            self.amount.clear()
            self.description.clear()
            self.load_table()

    """
    Delete selected entry from SQL database based on the entry id
    """
    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to delete!")
            return
        
        entry_id = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(self, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return
        
        month = self.get_current_month_year()

        query = QSqlQuery()
        query.prepare(f"DELETE FROM '{month}' WHERE id = :entry_id")
        query.bindValue(":entry_id", entry_id)
        
        if not query.exec_():
            QMessageBox.warning(self, "Error", "Failed to delete entry: " + query.lastError().text())
        else:
            self.load_table()

        


"""
Income class
"""
class Income(QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join('ui', 'incomescreen.ui')
        loadUi(ui_path, self)
        self.monthlyView.clicked.connect(self.navigate_to_monthly_view)
        self.addExpenseView.clicked.connect(self.navigate_to_expense_view)

        self.addIncome.clicked.connect(self.add_entry)
        self.deleteIncome.clicked.connect(self.delete_entry)
        
        self.table = self.findChild(QTableWidget, "tableWidget")  # Update this with the actual name from the .ui file

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Entry Type", "Amount", "Description"])

        self.load_table()

    def navigate_to_monthly_view(self):
        monthly_view = WelcomeScreen()
        widget.addWidget(monthly_view)
        widget.setCurrentWidget(monthly_view)

    def navigate_to_expense_view(self):
        expense = Expense()
        widget.addWidget(expense)
        widget.setCurrentWidget(expense)

    """
    Get current month and year for table creation formated as "YYYY_MM"
    """
    def get_current_month_year(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year

    """
    Load table with entries from SQL database
    """
    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_month_year()
        query = QSqlQuery(f"SELECT * FROM '{month}' WHERE entry_type == 'income' ORDER BY date DESC")
        row = 0
        while query.next():
            entry_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            entry_type = query.value(3)
            amount = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(entry_id))) 
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(entry_type))
            self.table.setItem(row, 4, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 5, QTableWidgetItem(description))

            row += 1

    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        entry_type = "income"
        amount = self.amount.text()
        description = self.description.toPlainText()

        month = self.get_current_month_year()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, category, entry_type, amount, description) 
                            VALUES (:date, :category, :entry_type, :amount, :description)
                        """)
        
        query.bindValue(":date", date)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(self, "Add Entry Failed", f"Failed to add entry: {error}")
        else:
            self.date_box.setDate(QDate.currentDate())
            self.dropdown.setCurrentIndex(0)
            self.amount.clear()
            self.description.clear()
            self.load_table()

    """
    Delete selected entry from SQL database based on the entry id
    """
    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Entry Chosen", "Please select an entry to delete!")
            return
        
        entry_id = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(self, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return
        
        month = self.get_current_month_year()

        query = QSqlQuery()
        query.prepare(f"DELETE FROM '{month}' WHERE id = :entry_id")
        query.bindValue(":entry_id", entry_id)
        
        if not query.exec_():
            QMessageBox.warning(self, "Error", "Failed to delete entry: " + query.lastError().text())
        else:
            self.load_table()

        
"""
Create the database 
"""
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("budget.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not connect to your database")
    sys.exit(1)


"""
Main function to run the application
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1300)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Error occurred while running the application.")