import datetime
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView, QMessageBox
from database import Database
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QDate

class IncomeDialog(QDialog):

    entry_added = pyqtSignal()

    def __init__(self):
        super(IncomeDialog, self).__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), "views", "incomeDialog.ui")
        loadUi(ui_file_path, self)

        self.incomeDateEdit.setDate(QDate.currentDate())

        self.incomeAddPushButton.clicked.connect(self.add_entry)
        self.incomeCancelPushButton.clicked.connect(self.close)
    
    """
    Add new entry to SQL database from user input
    """
    def add_entry(self):
        date = self.incomeDateEdit.date().toString("yyyy-MM-dd")
        source = self.incomeSourceEdit.text().capitalize()
        category = self.incomeCategoryDropdown.currentText()
        entry_type = "Income"
        amount = self.incomeAmountSpinbox.text()
        description = self.incomeDescriptionTextEdit.toPlainText()
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
            self.incomeDateEdit.setDate(QDate.currentDate())
            self.incomeSourceEdit.clear() 
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
