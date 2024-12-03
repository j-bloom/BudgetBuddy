import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QMessageBox
from database import Database
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QDate

class IncomeDialog(QDialog):

    entry_added = pyqtSignal()

    def __init__(self):
        super(IncomeDialog, self).__init__()
        loadUi('incomeDialog.ui', self)
        self.incomeAddPushButton.clicked.connect(self.add_entry)
        self.incomeCancelPushButton.clicked.connect(self.close)
    
    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.incomeDateEdit.date().toString("yyyy-MM-dd")
        store_name = self.incomeStoreEdit.text() 
        category = self.incomeCategoryDropdown.currentText()
        entry_type = "income"
        amount = self.incomeAmountSpinbox.text()
        description = self.incomeDescriptionTextEdit.toPlainText()
        month = self.get_current_year_month()
        query = QSqlQuery()
        query.prepare(f"""INSERT INTO '{month}' (date, store_name, category, entry_type, amount, description) 
                            VALUES (:date, :store_name, :category, :entry_type, :amount, :description)
                        """)
        
        query.bindValue(":date", date)
        query.bindValue(":store_name", store_name)
        query.bindValue(":category", category)
        query.bindValue(":entry_type", entry_type)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec_():
            error = query.lastError().text()
            QMessageBox.warning(self, "Add Entry Failed", f"Failed to add entry: {error}")
        else:
            self.incomeDateEdit.setDate(QDate.currentDate())
            self.incomeStoreEdit.clear() 
            self.incomeCategoryDropdown.setCurrentIndex(0)
            self.incomeAmountSpinbox.clear()
            self.incomeDescriptionTextEdit.clear()
            self.entry_added.emit()
            self.close()

    """
    Get current year and month for table creation formated as "YYYY_MM"
    """
    def get_current_year_month(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year
