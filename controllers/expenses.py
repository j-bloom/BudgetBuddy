import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import QDate
import models
import os

class Expense(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        ui_path = os.path.join('ui', 'expensescreen.ui')
        loadUi(ui_path, self)
        self.date_box.setDate(QDate.currentDate())
        self.stacked_widget = stacked_widget

        self.monthlyView.clicked.connect(self.navigate_to_monthly_view)
        self.addIncomeView.clicked.connect(self.navigate_to_income_view)

        self.addExpense.clicked.connect(self.add_entry)
        self.deleteExpense.clicked.connect(self.delete_entry)
        
        self.table = self.findChild(QTableWidget, "tableWidget")  # Update this with the actual name from the .ui file

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Entry Type", "Amount", "Description"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.load_table()

    def navigate_to_monthly_view(self):
        from controllers.welcome import WelcomeScreen
        monthly_view = WelcomeScreen(self.stacked_widget)
        self.stacked_widget.addWidget(monthly_view)
        self.stacked_widget.setCurrentWidget(monthly_view)

    def navigate_to_income_view(self):
        from controllers.income import Income
        income = Income(self.stacked_widget)
        self.stacked_widget.addWidget(income)
        self.stacked_widget.setCurrentWidget(income)

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

        expenses = controllers.get_total_amounts(month, "expense")
        self.total_expense.setText(f"$ {expenses}")
        income = controllers.get_total_amounts(month, "income")
        self.total_income.setText(f"$ {income}")

    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        entry_type = "expense"
        amount = self.amount.text()
        description = self.description.toPlainText()

        transaction = models.Transaction(date, category, entry_type, amount, description)

        month = self.get_current_month_year()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, category, entry_type, amount, description) 
                            VALUES (:date, :category, :entry_type, :amount, :description)
                        """)
        
        transaction.bind_to_query(query)
        
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

        # Get the values of the selected row to identify the entry in the database
        date = self.table.item(selected_row, 0).text()
        category = self.table.item(selected_row, 1).text()
        entry_type = self.table.item(selected_row, 2).text()
        amount = self.table.item(selected_row, 3).text()
        description = self.table.item(selected_row, 4).text()

        confirm = QMessageBox.question(self, "Delete Entry", "Are you sure you want to delete this entry?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return

        transaction = models.Transaction(date, category, entry_type, amount, description)

        month = self.get_current_month_year()

        query = QSqlQuery()
        query.prepare(f"""DELETE FROM '{month}' WHERE 
                        date = :date AND 
                        category = :category AND 
                        entry_type = :entry_type AND 
                        amount = :amount AND 
                        description = :description
                      """)

        transaction.bind_to_query(query)

        if not query.exec_():
            QMessageBox.warning(self, "Error", "Failed to delete entry: " + query.lastError().text())
        else:
            self.load_table()  

