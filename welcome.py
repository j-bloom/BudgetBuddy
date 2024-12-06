import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QTableWidgetItem
from database import Database
from expenses import ExpenseDialog
from income import IncomeDialog
from PyQt5.QtSql import QSqlQuery

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('welcomescreen.ui', self)

        """
        Create the database table with the name of the current year and month,
        allowing the monthly overview to be displayed
        """
        db = Database()
        month = self.get_current_year_month()
        db.create_table(month)

        """
        Setup the table object to modify the header
        Stretch the header to fit the full width of the table
        """
        self.table = self.findChild(QTableWidget, "MonthlyTableOverview")

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        """
        Connect the income/expense buttons to their respective views/dialogs
        """
        self.addExpenseBtn.clicked.connect(self.display_expense_dialog)
        self.addIncomeBtn.clicked.connect(self.display_income_dialog)

        self.update_totals()
        self.load_table()
        

    def update_totals(self):
        month = self.get_current_year_month()
        expenses = self.get_total_amounts(month, "expense")
        self.totalExpensesAmount.setText(f"$ {expenses:.2f}")
        income = self.get_total_amounts(month, "income")
        self.totalIncomeAmount.setText(f"$ {income:.2f}")

    """
    Get current year and month for table creation formated as "YYYY_MM"
    """
    def get_current_year_month(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year
    
    def display_expense_dialog(self):
        expense_dialog = ExpenseDialog()
        expense_dialog.entry_added.connect(self.reload_table)
        expense_dialog.exec_()

    def display_income_dialog(self):
        income_dialog = IncomeDialog()
        income_dialog.entry_added.connect(self.reload_table)
        income_dialog.exec_()


    """
    Populate the monthly overview table with the data from the database
    """
    def load_table(self):
        self.table.setRowCount(0)
        month = self.get_current_year_month()
        query = QSqlQuery(f"SELECT * FROM '{month}' ORDER BY date DESC")
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
        self.update_totals()
        self.load_table()

    
    """
    Fetch and display total amounts for income and expenses
    """
    def get_total_amounts(self, month, entry_type):
        query = QSqlQuery()
        
        # Prepare and execute the SQL query to sum the amounts
        query.prepare(f"""
                    SELECT SUM(amount) 
                    FROM '{month}' 
                    WHERE entry_type = :entry_type
                    """)
        query.bindValue(":entry_type", entry_type)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(None, "Add Entry Failed", f"Failed to retrieve total amount: {error}")
            return 0.0

        # Move to the first row to retrieve the result
        if query.next():
            total = query.value(0)
            if total is None or total =="":
                total = float(0.0)
            return float(total)
        else:
            return float(0.0)  
