import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QTableWidget, QHeaderView
from database import Database

class IncomeDialog(QDialog):
    def __init__(self):
        super(IncomeDialog, self).__init__()
        loadUi('incomeDialog.ui', self)
