import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtSql import QSqlQuery
from controllers.expenses import Expense
from controllers.income import Income
import os

class WelcomeScreen(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join('ui', 'welcomescreen.ui')
        loadUi(ui_path, self)

        self.stacked_widget = stacked_widget

        self.addExpenseView.clicked.connect(self.navigate_to_expense_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

        month = self.get_current_month_year()
        self.create_table(month)

        self.table = self.findChild(QTableWidget, "tableWidget")  # Update this with the actual name from the .ui file

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Entry Type", "Amount", "Description"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.load_table()

    def navigate_to_expense_view(self):
        expense = Expense(self.stacked_widget)
        self.stacked_widget.addWidget(expense)
        self.stacked_widget.setCurrentWidget(expense)

    def navigate_to_income_view(self):
        income = Income(self.stacked_widget)
        self.stacked_widget.addWidget(income)
        self.stacked_widget.setCurrentWidget(income)

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
            date = query.value(1)
            category = query.value(2)
            entry_type = query.value(3)
            amount = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(category))
            self.table.setItem(row, 2, QTableWidgetItem(entry_type))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1