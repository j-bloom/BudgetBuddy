import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QAbstractItemView, QVBoxLayout, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
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

        self.main_window.export_pdf.clicked.connect(self.functions.handle_export_pdf)
        self.main_window.export_csv.clicked.connect(self.functions.handle_export_csv)
        self.main_window.import_csv.clicked.connect(self.functions.handle_import_csv)
        self.main_window.import_screenshot.clicked.connect(self.functions.handle_import_screenshot)

        self.main_window.view_month_btn.clicked.connect(self.functions.open_table_search_dialog)
        self.main_window.add_expense_btn.clicked.connect(self.functions.open_add_expense_dialog)
        self.main_window.add_income_btn.clicked.connect(self.functions.open_add_income_dialog)
        self.main_window.edit_entry_btn.clicked.connect(self.functions.open_edit_dialog)
        self.main_window.duplicate_entry_btn.clicked.connect(self.functions.duplicate_selected_entry)
        self.main_window.delete_entry_btn.clicked.connect(self.db.delete_entry)

        
        self.main_window.source_dropdown.addItem("All")
        self.main_window.source_dropdown.addItems(self.db.get_unique_sources())

        self.main_window.source_dropdown.setCurrentText("All")
        self.main_window.source_dropdown.currentTextChanged.connect(self.functions.filter_by_source)

        self.main_window.entry_type_dropdown.addItems(["All", "Expense", "Income"])

        self.main_window.entry_type_dropdown.setCurrentText("All")
        self.main_window.entry_type_dropdown.currentTextChanged.connect(self.functions.filter_by_entry_type)

        self.main_window.category_dropdown.addItems(["All", "Groceries", "Bills", "Transportion", "Gas", "Car maintenance", "Rent", "Pets", "Salary", "Bonus", "Freelance", "Investments", "Gift"])
        self.main_window.category_dropdown.currentTextChanged.connect(self.functions.filter_by_category)

        self.main_window.min_amount_spinbox.valueChanged.connect(self.functions.apply_numeric_filter)
        self.main_window.max_amount_spinbox.valueChanged.connect(self.functions.apply_numeric_filter)

        self.main_window.description_input.textChanged.connect(self.functions.filter_by_description)
        self.main_window.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_window.table.cellDoubleClicked.connect(self.functions.handle_double_click)

        self.main_window.filter_search.textChanged.connect(self.functions.filter_table)
        self.main_window.clear_filter_btn.clicked.connect(self.functions.clear_filters)

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