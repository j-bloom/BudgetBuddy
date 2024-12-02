import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView
from database import Database

class ExpenseDialog(QDialog):
    def __init__(self):
        super(ExpenseDialog, self).__init__()
        loadUi('expenseDialog.ui', self)
