import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from ui.main_window import MainWindow
from database.database import Database
from controllers.functions import Functions

# App Class
class BudgetBuddyApp(QWidget):
    def __init__(self):
        # Main App Objects and Settings
        super().__init__()
        self.setWindowTitle("Budget Tracker 2.0")
        self.resize(550, 500)

        self.main_window = MainWindow()
        self.db = Database(self.main_window)
        self.functions = Functions(self.main_window, self.db)

        self.main_window.view_month_btn.clicked.connect(self.functions.open_table_search_dialog)
        self.main_window.add_expense_btn.clicked.connect(self.functions.open_add_expense_dialog)
        self.main_window.add_income_btn.clicked.connect(self.functions.open_add_income_dialog)
        self.main_window.edit_entry_btn.clicked.connect(self.functions.open_edit_dialog)
        self.main_window.duplicate_entry_btn.clicked.connect(self.functions.duplicate_selected_entry)
        self.main_window.delete_entry_btn.clicked.connect(self.db.delete_entry)

        # Add main_window to this widget's layout
        layout = QVBoxLayout()
        layout.addWidget(self.main_window)
        self.setLayout(layout)

        self.db.load_table()

# Show/Run our App
if __name__ in "__main__":
    app = QApplication([])
    main = BudgetBuddyApp()
    main.show()
    app.exec_() 