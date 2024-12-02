import datetime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from database import Database

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('welcomescreen.ui', self)
        db = Database()
        month = self.get_current_month_year()
        db.create_table(month)

        
    """
    Get current month and year for table creation formated as "YYYY_MM"
    """
    def get_current_month_year(self):
        today = datetime.datetime.now()
        current_month_year = today.strftime("%Y_%m")
        return current_month_year