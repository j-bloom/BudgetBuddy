import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QMessageBox
from database import Database
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QDate

class ExpenseDialog(QDialog):
    
    entry_added = pyqtSignal()

    def __init__(self):
        super(ExpenseDialog, self).__init__()
        loadUi('expenseDialog.ui', self)
        self.expenseAddPushButton.clicked.connect(self.add_entry)
        self.expenseCancelPushButton.clicked.connect(self.close)
    
    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.expenseDateEdit.date().toString("yyyy-MM-dd")
        source = self.expenseSourceEdit.text() 
        category = self.expenseCategoryDropdown.currentText()
        entry_type = "expense"
        amount = self.expenseAmountSpinbox.text()
        description = self.expenseDescriptionTextEdit.toPlainText()
        month = self.get_current_year_month()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, source, category, entry_type, amount, description) 
                            VALUES (:date, :source, :category, :entry_type, :amount, :description)
                        """)
        
        query.bindValue(":date", date)
        query.bindValue(":source", source)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(self, "Add Entry Failed", f"Failed to add entry: {error}")
        else:
            self.expenseDateEdit.setDate(QDate.currentDate())
            self.expenseSourceEdit.clear() 
            self.expenseCategoryDropdown.setCurrentIndex(0)
            self.expenseAmountSpinbox.clear()
            self.expenseDescriptionTextEdit.clear()
            self.entry_added.emit()
            self.close()

    """
    Get current year and month for table creation formated as "YYYY_MM"
    """
    def get_current_year_month(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year
